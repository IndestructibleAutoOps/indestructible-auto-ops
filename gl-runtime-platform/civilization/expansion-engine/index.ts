/**
 * @GL-governed
 * @version 21.0.0
 * @priority 2
 * @stage complete
 */
/**
 * GL Runtime Platform v13.0.0
 * Module: Expansion Engine
 * 
 * The expansion engine enables the civilization to expand into new projects,
 * organizations, clusters, languages, and domains while preserving its core
 * values and culture.
 * 
 * Key Capabilities:
 * - Cross-project expansion
 * - Cross-organization expansion
 * - Cross-cluster expansion
 * - Cross-language expansion
 * - Cross-domain expansion
 * - Cultural preservation during expansion
 * - Expansion success tracking
 */

import { EventEmitter } from 'events';

// ============================================================================
// Core Types
// ============================================================================

export interface ExpansionTarget {
  id: string;
  type: 'project' | 'organization' | 'cluster' | 'language' | 'domain';
  name: string;
  description: string;
  location: string;
  readiness: number; // 0-1, how ready for expansion
  complexity: number; // 0-1
  culturalFit: number; // 0-1
  estimatedDuration: number; // milliseconds
  prerequisites: string[];
}

export interface ExpansionCampaign {
  id: string;
  targetId: string;
  name: string;
  description: string;
  status: 'planning' | 'in_progress' | 'completed' | 'failed' | 'paused';
  phase: 'assessment' | 'preparation' | 'deployment' | 'integration' | 'stabilization';
  startTime: number;
  endTime?: number;
  progress: number; // 0-1
  successRate: number; // 0-1
  challenges: string[];
  achievements: string[];
  culturalPreservation: number; // 0-1
}

export interface ExpansionMetric {
  id: string;
  campaignId: string;
  type: 'speed' | 'efficiency' | 'success' | 'integration' | 'cultural_alignment';
  value: number; // 0-1
  timestamp: number;
  trend: 'improving' | 'stable' | 'declining';
}

export interface ExpansionStrategy {
  id: string;
  name: string;
  description: string;
  targetType: ExpansionTarget['type'];
  approach: 'gradual' | 'aggressive' | 'collaborative' | 'adaptive';
  successRate: number; // 0-1
  avgDuration: number; // milliseconds
  culturalRisk: number; // 0-1
  applicability: string[];
}

export interface ExpansionEvent {
  id: string;
  type: 'target_discovered' | 'campaign_created' | 'phase_completed' |
        'challenge_encountered' | 'achievement_unlocked' | 'expansion_completed' |
        'expansion_failed' | 'cultural_drift_detected';
  timestamp: number;
  campaignId?: string;
  description: string;
  impact: number; // -1 to 1
  metadata: Record<string, any>;
}

export interface ExpansionState {
  targets: ExpansionTarget[];
  campaigns: ExpansionCampaign[];
  strategies: ExpansionStrategy[];
  metrics: ExpansionMetric[];
  events: ExpansionEvent[];
  overallSuccess: number; // 0-1
  expansionVelocity: number; // expansions per day
}

// ============================================================================
// Main Expansion Engine Class
// ============================================================================

export class ExpansionEngine extends EventEmitter {
  private targets: Map<string, ExpansionTarget> = new Map();
  private campaigns: Map<string, ExpansionCampaign> = new Map();
  private strategies: Map<string, ExpansionStrategy> = new Map();
  private metrics: Map<string, ExpansionMetric> = new Map();
  private events: ExpansionEvent[] = [];
  
  // Configuration
  private readonly MAX_TARGETS = 100;
  private readonly MAX_CAMPAIGNS = 50;
  private readonly MAX_STRATEGIES = 20;
  private readonly MAX_METRICS = 500;
  private readonly EVENT_RETENTION_DAYS = 365;
  
  // Metrics
  private overallSuccess: number = 0.5;
  private expansionVelocity: number = 0;
  private evolutionCycles: number = 0;

  constructor() {
    super();
    this.initializeExpansion();
  }

  // ==========================================================================
  // Initialization
  // ==========================================================================

  private initializeExpansion(): void {
    // Define expansion strategies
    this.defineStrategies();
    
    // Start monitoring
    this.startMonitoring();
    
    this.emit('expansion_initialized', {
      strategies: this.strategies.size,
      targets: this.targets.size
    });
  }

  private defineStrategies(): void {
    const strategies: Omit<ExpansionStrategy, 'id'>[] = [
      {
        name: 'Gradual Integration',
        description: 'Gradually integrate with the target, preserving existing culture while introducing civilization values',
        targetType: 'project',
        approach: 'gradual',
        successRate: 0.85,
        avgDuration: 7 * 24 * 60 * 60 * 1000, // 7 days
        culturalRisk: 0.2,
        applicability: ['small_projects', 'existing_teams']
      },
      {
        name: 'Aggressive Deployment',
        description: 'Rapidly deploy civilization infrastructure to the target',
        targetType: 'organization',
        approach: 'aggressive',
        successRate: 0.75,
        avgDuration: 3 * 24 * 60 * 60 * 1000, // 3 days
        culturalRisk: 0.5,
        applicability: ['new_organizations', 'greenfield_projects']
      },
      {
        name: 'Collaborative Partnership',
        description: 'Establish partnership with target organization, collaborating on mutual goals',
        targetType: 'organization',
        approach: 'collaborative',
        successRate: 0.9,
        avgDuration: 14 * 24 * 60 * 60 * 1000, // 14 days
        culturalRisk: 0.15,
        applicability: ['established_organizations', 'partnerships']
      },
      {
        name: 'Adaptive Expansion',
        description: 'Adapt expansion approach based on target characteristics and feedback',
        targetType: 'cluster',
        approach: 'adaptive',
        successRate: 0.88,
        avgDuration: 10 * 24 * 60 * 60 * 1000, // 10 days
        culturalRisk: 0.25,
        applicability: ['complex_environments', 'multi_cluster_scenarios']
      },
      {
        name: 'Language Bridge',
        description: 'Establish language bridges to enable cross-language expansion',
        targetType: 'language',
        approach: 'gradual',
        successRate: 0.82,
        avgDuration: 5 * 24 * 60 * 60 * 1000, // 5 days
        culturalRisk: 0.3,
        applicability: ['new_languages', 'language_transitions']
      },
      {
        name: 'Domain Pioneer',
        description: 'Pioneer expansion into new domains with minimal existing infrastructure',
        targetType: 'domain',
        approach: 'aggressive',
        successRate: 0.78,
        avgDuration: 12 * 24 * 60 * 60 * 1000, // 12 days
        culturalRisk: 0.4,
        applicability: ['new_domains', 'emerging_technologies']
      }
    ];

    strategies.forEach(strategy => {
      this.strategies.set(
        `strat_${strategy.name.toLowerCase().replace(/\s+/g, '_')}`,
        { ...strategy, id: `strat_${strategy.name.toLowerCase().replace(/\s+/g, '_')}` }
      );
    });
  }

  // ==========================================================================
  // Target Management
  // ==========================================================================

  public discoverTarget(targetData: Omit<ExpansionTarget, 'id'>): string {
    if (this.targets.size >= this.MAX_TARGETS) {
      this.pruneTargets();
    }

    const target: ExpansionTarget = {
      ...targetData,
      id: `target_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
    };

    this.targets.set(target.id, target);
    this.recordEvent({
      type: 'target_discovered',
      description: `Expansion target discovered: ${target.name} (${target.type})`,
      impact: 0.05,
      metadata: { targetId: target.id, type: target.type, readiness: target.readiness }
    });

    this.emit('target_discovered', target);
    return target.id;
  }

  public assessTarget(targetId: string): { ready: boolean; confidence: number } {
    const target = this.targets.get(targetId);
    if (!target) {
      return { ready: false, confidence: 0 };
    }

    // Calculate readiness based on multiple factors
    const readinessScore = (
      target.readiness * 0.4 +
      target.culturalFit * 0.3 +
      (1 - target.complexity) * 0.3
    );

    const ready = readinessScore > 0.6 && target.prerequisites.length === 0;
    const confidence = readinessScore;

    return { ready, confidence };
  }

  private pruneTargets(): void {
    const lowReadinessTargets = Array.from(this.targets.values())
      .filter(t => t.readiness < 0.3 && t.culturalFit < 0.3)
      .sort((a, b) => a.readiness - b.readiness);

    if (lowReadinessTargets.length > 0) {
      this.targets.delete(lowReadinessTargets[0].id);
    }
  }

  // ==========================================================================
  // Campaign Management
  // ==========================================================================

  public createCampaign(campaignData: {
    targetId: string;
    name: string;
    description: string;
    strategyId?: string;
  }): string {
    if (this.campaigns.size >= this.MAX_CAMPAIGNS) {
      this.pruneCampaigns();
    }

    const target = this.targets.get(campaignData.targetId);
    if (!target) {
      return '';
    }

    const strategy = campaignData.strategyId 
      ? this.strategies.get(campaignData.strategyId)
      : null;

    const campaign: ExpansionCampaign = {
      id: `campaign_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      targetId: campaignData.targetId,
      name: campaignData.name,
      description: campaignData.description,
      status: 'planning',
      phase: 'assessment',
      startTime: Date.now(),
      progress: 0,
      successRate: strategy?.successRate || 0.7,
      challenges: [],
      achievements: [],
      culturalPreservation: target.culturalFit
    };

    this.campaigns.set(campaign.id, campaign);
    this.recordEvent({
      type: 'campaign_created',
      campaignId: campaign.id,
      description: `Expansion campaign created: ${campaign.name}`,
      impact: 0.1,
      metadata: { campaignId: campaign.id, targetId: campaign.targetId, strategy: strategy?.name }
    });

    this.emit('campaign_created', campaign);

    // Start campaign execution
    this.executeCampaign(campaign.id);

    return campaign.id;
  }

  private executeCampaign(campaignId: string): void {
    const campaign = this.campaigns.get(campaignId);
    if (!campaign) return;

    campaign.status = 'in_progress';

    // Simulate campaign phases
    this.executeCampaignPhase(campaignId, 'assessment', 2000);
  }

  private executeCampaignPhase(campaignId: string, phase: ExpansionCampaign['phase'], duration: number): void {
    const campaign = this.campaigns.get(campaignId);
    if (!campaign) return;

    campaign.phase = phase;

    setTimeout(() => {
      // Record phase completion
      this.recordEvent({
        type: 'phase_completed',
        campaignId: campaignId,
        description: `Campaign phase "${phase}" completed`,
        impact: 0.05,
        metadata: { campaignId, phase, progress: campaign.progress }
      });

      // Determine next phase or completion
      const phases: ExpansionCampaign['phase'][] = ['assessment', 'preparation', 'deployment', 'integration', 'stabilization'];
      const currentPhaseIndex = phases.indexOf(phase);

      if (currentPhaseIndex < phases.length - 1) {
        // Move to next phase
        campaign.progress = (currentPhaseIndex + 1) / phases.length;
        const nextPhase = phases[currentPhaseIndex + 1];
        const nextDuration = duration + Math.random() * 2000;
        this.executeCampaignPhase(campaignId, nextPhase, nextDuration);
      } else {
        // Campaign completed
        this.completeCampaign(campaignId);
      }
    }, duration);
  }

  private completeCampaign(campaignId: string): void {
    const campaign = this.campaigns.get(campaignId);
    if (!campaign) return;

    const success = Math.random() > 0.2;
    campaign.status = success ? 'completed' : 'failed';
    campaign.endTime = Date.now();
    campaign.progress = 1;
    campaign.successRate = success ? campaign.successRate : Math.random() * 0.5;

    this.recordEvent({
      type: success ? 'expansion_completed' : 'expansion_failed',
      campaignId: campaignId,
      description: `Campaign "${campaign.name}" ${success ? 'completed successfully' : 'failed'}`,
      impact: success ? 0.2 : -0.15,
      metadata: { 
        campaignId, 
        success, 
        duration: campaign.endTime! - campaign.startTime,
        culturalPreservation: campaign.culturalPreservation
      }
    });

    this.emit(success ? 'expansion_completed' : 'expansion_failed', campaign);
  }

  private pruneCampaigns(): void {
    const completedCampaigns = Array.from(this.campaigns.values())
      .filter(c => c.status === 'completed' || c.status === 'failed')
      .sort((a, b) => (a.endTime || 0) - (b.endTime || 0));

    while (completedCampaigns.length > this.MAX_CAMPAIGNS / 2 && this.campaigns.size >= this.MAX_CAMPAIGNS) {
      const toRemove = completedCampaigns.shift();
      if (toRemove) {
        this.campaigns.delete(toRemove.id);
      }
    }
  }

  // ==========================================================================
  // Metric Tracking
  // ==========================================================================

  public recordMetric(metricData: Omit<ExpansionMetric, 'id' | 'timestamp'>): void {
    if (this.metrics.size >= this.MAX_METRICS) {
      this.pruneMetrics();
    }

    const previousMetric = Array.from(this.metrics.values())
      .filter(m => m.campaignId === metricData.campaignId && m.type === metricData.type)
      .sort((a, b) => b.timestamp - a.timestamp)[0];

    const trend = previousMetric
      ? metricData.value > previousMetric.value ? 'improving' :
        metricData.value < previousMetric.value ? 'declining' : 'stable'
      : 'stable';

    const metric: ExpansionMetric = {
      ...metricData,
      id: `metric_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      timestamp: Date.now(),
      trend
    };

    this.metrics.set(metric.id, metric);
  }

  private pruneMetrics(): void {
    const oldMetrics = Array.from(this.metrics.values())
      .filter(m => Date.now() - m.timestamp > 90 * 24 * 60 * 60 * 1000) // 90 days
      .sort((a, b) => a.timestamp - b.timestamp);

    while (oldMetrics.length > 0 && this.metrics.size >= this.MAX_METRICS) {
      const toRemove = oldMetrics.shift();
      if (toRemove) {
        this.metrics.delete(toRemove.id);
      }
    }
  }

  // ==========================================================================
  // Monitoring
  // ==========================================================================

  private startMonitoring(): void {
    // Run monitoring every 60 seconds
    setInterval(() => {
      this.evolutionCycles++;
      this.monitorExpansion();
    }, 60000);
  }

  private monitorExpansion(): void {
    // Update metrics
    this.updateMetrics();

    // Calculate expansion velocity
    this.calculateExpansionVelocity();

    this.emit('expansion_monitored', {
      cycle: this.evolutionCycles,
      targets: this.targets.size,
      campaigns: this.campaigns.size,
      success: this.overallSuccess,
      velocity: this.expansionVelocity
    });
  }

  private updateMetrics(): void {
    const completedCampaigns = Array.from(this.campaigns.values())
      .filter(c => c.status === 'completed');

    if (completedCampaigns.length > 0) {
      const successRate = completedCampaigns.filter(c => c.successRate > 0.7).length / completedCampaigns.length;
      this.overallSuccess = successRate;
    }

    // Record current metrics for all active campaigns
    this.campaigns.forEach(campaign => {
      if (campaign.status === 'in_progress') {
        this.recordMetric({
          campaignId: campaign.id,
          type: 'success',
          value: campaign.progress * campaign.successRate,
          trend: 'stable'
        });
        this.recordMetric({
          campaignId: campaign.id,
          type: 'integration',
          value: campaign.culturalPreservation,
          trend: 'stable'
        });
      }
    });
  }

  private calculateExpansionVelocity(): void {
    const recentCompletions = Array.from(this.campaigns.values())
      .filter(c => c.status === 'completed' && c.endTime && (Date.now() - c.endTime) < 7 * 24 * 60 * 60 * 1000); // Last 7 days

    this.expansionVelocity = recentCompletions.length / 7; // Expansions per day
  }

  // ==========================================================================
  // Event Management
  // ==========================================================================

  private recordEvent(event: Omit<ExpansionEvent, 'id' | 'timestamp'>): void {
    const fullEvent: ExpansionEvent = {
      ...event,
      id: `evt_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      timestamp: Date.now()
    };

    this.events.push(fullEvent);

    // Prune old events
    const cutoffTime = Date.now() - (this.EVENT_RETENTION_DAYS * 24 * 60 * 60 * 1000);
    this.events = this.events.filter(e => e.timestamp > cutoffTime);
  }

  // ==========================================================================
  // Public API
  // ==========================================================================

  public getState(): ExpansionState {
    return {
      targets: Array.from(this.targets.values()),
      campaigns: Array.from(this.campaigns.values()),
      strategies: Array.from(this.strategies.values()),
      metrics: Array.from(this.metrics.values()),
      events: this.events,
      overallSuccess: this.overallSuccess,
      expansionVelocity: this.expansionVelocity
    };
  }

  public getTargets(): ExpansionTarget[] {
    return Array.from(this.targets.values());
  }

  public getCampaigns(): ExpansionCampaign[] {
    return Array.from(this.campaigns.values());
  }

  public getStrategies(): ExpansionStrategy[] {
    return Array.from(this.strategies.values());
  }

  public getMetrics(): ExpansionMetric[] {
    return Array.from(this.metrics.values());
  }

  public getEvents(limit?: number): ExpansionEvent[] {
    return limit ? this.events.slice(-limit) : this.events;
  }

  public getStatistics(): {
    targets: number;
    campaigns: number;
    strategies: number;
    metrics: number;
    events: number;
    overallSuccess: number;
    expansionVelocity: number;
    evolutionCycles: number;
  } {
    return {
      targets: this.targets.size,
      campaigns: this.campaigns.size,
      strategies: this.strategies.size,
      metrics: this.metrics.size,
      events: this.events.length,
      overallSuccess: this.overallSuccess,
      expansionVelocity: this.expansionVelocity,
      evolutionCycles: this.evolutionCycles
    };
  }
}