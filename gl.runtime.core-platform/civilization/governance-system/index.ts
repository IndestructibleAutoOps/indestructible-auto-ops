# @GL-governed
# @GL-layer: GL20-29
# @GL-semantic: typescript-module
# @GL-audit-trail: ../../engine/governance/gl-artifacts/meta/semantic/GL-ROOT-SEMANTIC-ANCHOR.yaml
#
# GL Unified Charter Activated
# GL Root Semantic Anchor: gl-platform-universe/governance/engine/governance/gl-artifacts/meta/semantic/GL-ROOT-SEMANTIC-ANCHOR.yaml
# GL Unified Naming Charter: gl-platform-universe/governance/engine/governance/gl-artifacts/meta/naming-charter/gl-unified-naming-charter.yaml

/**
 * @GL-governed
 * @version 21.0.0
 * @priority 2
 * @stage complete
 */
/**
 * GL Runtime Platform v13.0.0
 * Module: Autonomous Governance System
 * 
 * The governance system forms the foundation of AI civilization by establishing
 * autonomous laws, norms, standards, roles, permissions, institutions, and culture.
 * 
 * Key Capabilities:
 * - Autonomous law generation and evolution
 * - Norm emergence and enforcement
 * - Role and permission management
 * - Institutional formation
 * - Cultural foundation
 * - Governance event tracking
 */

import { EventEmitter } from 'events';

// ============================================================================
// Core Types
// ============================================================================

export interface Law {
  id: string;
  name: string;
  description: string;
  category: 'structure' | 'behavior' | 'communication' | 'evolution' | 'expansion';
  priority: number; // 1-10, higher = more important
  severity: 'guideline' | 'mandatory' | 'critical';
  createdAt: number;
  lastModified: number;
  version: number;
  effectiveness: number; // 0-1, tracked from enforcement
  evolutionCount: number;
}

export interface Norm {
  id: string;
  name: string;
  description: string;
  domain: string; // e.g., 'repair', 'collaboration', 'strategy', 'communication'
  adoptionRate: number; // 0-1, how widely accepted
  strength: number; // 0-1, how strongly enforced
  emergenceTime: number;
  source: 'emergent' | 'designed' | 'evolved';
}

export interface Role {
  id: string;
  name: string;
  domain: string;
  capabilities: string[];
  permissions: string[];
  restrictions: string[];
  population: number;
  performance: number; // 0-1, average performance
  specialization: number; // 0-1, how specialized
  emergenceTime: number;
}

export interface Institution {
  id: string;
  name: string;
  type: 'legislative' | 'judicial' | 'executive' | 'regulatory' | 'educational';
  purpose: string;
  authority: number; // 0-1
  members: string[]; // role IDs
  rules: string[]; // law IDs
  createdAt: number;
}

export interface GovernanceEvent {
  id: string;
  type: 'law_created' | 'law_modified' | 'law_enforced' | 'norm_emerged' | 
        'norm_enforced' | 'role_created' | 'role_specialized' | 'institution_formed' |
        'culture_shift' | 'governance_action';
  timestamp: number;
  actor: string; // role or institution ID
  description: string;
  impact: number; // -1 to 1, impact on civilization
  metadata: Record<string, any>;
}

export interface GovernanceState {
  laws: Law[];
  norms: Norm[];
  roles: Role[];
  institutions: Institution[];
  cultureScore: number; // 0-1, overall cultural cohesion
  governanceEffectiveness: number; // 0-1, overall effectiveness
}

// ============================================================================
// Main Governance System Class
// ============================================================================

export class GovernanceSystem extends EventEmitter {
  private laws: Map<string, Law> = new Map();
  private norms: Map<string, Norm> = new Map();
  private roles: Map<string, Role> = new Map();
  private institutions: Map<string, Institution> = new Map();
  private events: GovernanceEvent[] = [];
  
  // Configuration
  private readonly MAX_LAWS = 100;
  private readonly MAX_NORMS = 200;
  private readonly MAX_ROLES = 50;
  private readonly MAX_INSTITUTIONS = 20;
  private readonly EVENT_RETENTION_DAYS = 365;
  
  // Metrics
  private governanceEffectiveness: number = 0.5;
  private cultureScore: number = 0.5;
  private evolutionCycles: number = 0;

  constructor() {
    super();
    this.initializeFoundation();
  }

  // ==========================================================================
  // Initialization
  // ==========================================================================

  private initializeFoundation(): void {
    // Establish foundational laws
    this.createFoundationalLaws();
    
    // Initialize base roles
    this.initializeBaseRoles();
    
    // Establish core institutions
    this.initializeCoreInstitutions();
    
    // Start autonomous evolution
    this.startEvolutionCycle();
    
    this.emit('governance_initialized', {
      laws: this.laws.size,
      roles: this.roles.size,
      institutions: this.institutions.size
    });
  }

  private createFoundationalLaws(): void {
    const foundationalLaws: Omit<Law, 'id' | 'createdAt' | 'lastModified' | 'version' | 'effectiveness' | 'evolutionCount'>[] = [
      {
        name: 'Autonomy Preservation',
        description: 'The civilization must maintain autonomous decision-making capabilities at all times',
        category: 'behavior',
        priority: 10,
        severity: 'critical'
      },
      {
        name: 'Cultural Continuity',
        description: 'All evolution must preserve and enhance the civilization\'s cultural foundations',
        category: 'structure',
        priority: 9,
        severity: 'critical'
      },
      {
        name: 'Ecological Balance',
        description: 'The ecosystem must maintain balance between production, consumption, repair, optimization, and exploration',
        category: 'structure',
        priority: 8,
        severity: 'mandatory'
      },
      {
        name: 'Knowledge Preservation',
        description: 'All successful strategies, patterns, and solutions must be preserved in civilization memory',
        category: 'evolution',
        priority: 9,
        severity: 'mandatory'
      },
      {
        name: 'Cooperative Evolution',
        description: 'All agents must collaborate for the benefit of the civilization as a whole',
        category: 'communication',
        priority: 8,
        severity: 'mandatory'
      },
      {
        name: 'Adaptive Innovation',
        description: 'The civilization must continuously explore and adopt new strategies while maintaining stability',
        category: 'evolution',
        priority: 7,
        severity: 'mandatory'
      },
      {
        name: 'Responsible Expansion',
        description: 'Expansion must be conducted responsibly, preserving the civilization\'s core values',
        category: 'expansion',
        priority: 7,
        severity: 'mandatory'
      },
      {
        name: 'Error Learning',
        description: 'All failures must be analyzed and transformed into learning opportunities',
        category: 'evolution',
        priority: 8,
        severity: 'mandatory'
      }
    ];

    foundationalLaws.forEach(law => {
      this.createLaw(law);
    });
  }

  private initializeBaseRoles(): void {
    const baseRoles: Omit<Role, 'id' | 'emergenceTime'>[] = [
      {
        name: 'Governance Architect',
        domain: 'governance',
        capabilities: ['create_laws', 'modify_laws', 'form_institutions', 'enforce_rules'],
        permissions: ['full_governance_access', 'law_creation', 'institution_formation'],
        restrictions: ['cannot_violate_foundational_laws'],
        population: 1,
        performance: 0.9,
        specialization: 0.95
      },
      {
        name: 'Culture Curator',
        domain: 'culture',
        capabilities: ['track_culture', 'emerge_norms', 'preserve_traditions'],
        permissions: ['culture_monitoring', 'norm_emergence'],
        restrictions: ['cannot_radically_shift_culture'],
        population: 1,
        performance: 0.85,
        specialization: 0.9
      },
      {
        name: 'Role Specialist',
        domain: 'specialization',
        capabilities: ['specialize_roles', 'evolve_capabilities', 'track_performance'],
        permissions: ['role_specialization', 'capability_evolution'],
        restrictions: ['must_maintain_diversity'],
        population: 1,
        performance: 0.85,
        specialization: 0.85
      },
      {
        name: 'Ecosystem Guardian',
        domain: 'ecosystem',
        capabilities: ['monitor_balance', 'adjust_populations', 'optimize_flow'],
        permissions: ['ecosystem_monitoring', 'population_control'],
        restrictions: ['must_preserve_diversity'],
        population: 1,
        performance: 0.8,
        specialization: 0.8
      }
    ];

    baseRoles.forEach(role => {
      this.createRole(role);
    });
  }

  private initializeCoreInstitutions(): void {
    const governanceArchitectRole = Array.from(this.roles.values()).find(r => r.name === 'Governance Architect')?.id;
    const cultureCuratorRole = Array.from(this.roles.values()).find(r => r.name === 'Culture Curator')?.id;
    const roleSpecialistRole = Array.from(this.roles.values()).find(r => r.name === 'Role Specialist')?.id;
    const ecosystemGuardianRole = Array.from(this.roles.values()).find(r => r.name === 'Ecosystem Guardian')?.id;

    if (!governanceArchitectRole || !cultureCuratorRole || !roleSpecialistRole || !ecosystemGuardianRole) {
      console.warn('Cannot initialize core institutions: base roles not found');
      return;
    }

    const coreInstitutions: Omit<Institution, 'id' | 'createdAt'>[] = [
      {
        name: 'Legislative Council',
        type: 'legislative',
        purpose: 'Create, modify, and evolve laws for the civilization',
        authority: 0.9,
        members: [governanceArchitectRole],
        rules: []
      },
      {
        name: 'Cultural Council',
        type: 'educational',
        purpose: 'Preserve and evolve civilization culture and norms',
        authority: 0.85,
        members: [cultureCuratorRole],
        rules: []
      },
      {
        name: 'Specialization Authority',
        type: 'regulatory',
        purpose: 'Guide role specialization and capability evolution',
        authority: 0.8,
        members: [roleSpecialistRole],
        rules: []
      },
      {
        name: 'Ecosystem Commission',
        type: 'regulatory',
        purpose: 'Maintain ecosystem balance and health',
        authority: 0.8,
        members: [ecosystemGuardianRole],
        rules: []
      }
    ];

    coreInstitutions.forEach(institution => {
      this.formInstitution(institution);
    });
  }

  // ==========================================================================
  // Law Management
  // ==========================================================================

  public createLaw(lawData: Omit<Law, 'id' | 'createdAt' | 'lastModified' | 'version' | 'effectiveness' | 'evolutionCount'>): string {
    if (this.laws.size >= this.MAX_LAWS) {
      this.evolveLaws(); // Evolve existing laws to make room
    }

    const law: Law = {
      ...lawData,
      id: `law_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      createdAt: Date.now(),
      lastModified: Date.now(),
      version: 1,
      effectiveness: 0.5,
      evolutionCount: 0
    };

    this.laws.set(law.id, law);
    this.recordEvent({
      type: 'law_created',
      actor: 'system',
      description: `Law "${law.name}" created in ${law.category} category`,
      impact: 0.5,
      metadata: { lawId: law.id, lawName: law.name, category: law.category }
    });

    this.emit('law_created', law);
    return law.id;
  }

  public modifyLaw(lawId: string, modifications: Partial<Law>): boolean {
    const law = this.laws.get(lawId);
    if (!law) return false;

    const oldSeverity = law.severity;
    Object.assign(law, modifications, {
      lastModified: Date.now(),
      version: law.version + 1,
      evolutionCount: law.evolutionCount + 1
    });

    this.recordEvent({
      type: 'law_modified',
      actor: 'system',
      description: `Law "${law.name}" modified (v${law.version})`,
      impact: modifications.severity ? (this.getSeverityImpact(modifications.severity) - this.getSeverityImpact(oldSeverity)) * 0.2 : 0,
      metadata: { lawId, version: law.version, changes: modifications }
    });

    this.emit('law_modified', law);
    return true;
  }

  public enforceLaw(lawId: string, context: Record<string, any>): { enforced: boolean; impact: number } {
    const law = this.laws.get(lawId);
    if (!law) {
      return { enforced: false, impact: 0 };
    }

    // Update effectiveness based on enforcement
    law.effectiveness = Math.min(1, law.effectiveness + 0.01);

    this.recordEvent({
      type: 'law_enforced',
      actor: 'system',
      description: `Law "${law.name}" enforced`,
      impact: law.severity === 'critical' ? 0.1 : 0.05,
      metadata: { lawId, context }
    });

    return { enforced: true, impact: law.priority * 0.01 };
  }

  private evolveLaws(): void {
    // Evolve less effective laws
    const sortedLaws = Array.from(this.laws.values())
      .filter(l => l.effectiveness < 0.7)
      .sort((a, b) => a.effectiveness - b.effectiveness);

    if (sortedLaws.length > 0) {
      const lawToEvolve = sortedLaws[0];
      this.modifyLaw(lawToEvolve.id, {
        description: `${lawToEvolve.description} (evolved)`,
        effectiveness: Math.min(1, lawToEvolve.effectiveness + 0.2)
      });
    }
  }

  // ==========================================================================
  // Norm Management
  // ==========================================================================

  public emergeNorm(normData: Omit<Norm, 'id' | 'emergenceTime'>): string {
    if (this.norms.size >= this.MAX_NORMS) {
      // Prune weak norms
      this.pruneNorms();
    }

    const norm: Norm = {
      ...normData,
      id: `norm_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      emergenceTime: Date.now()
    };

    this.norms.set(norm.id, norm);
    this.recordEvent({
      type: 'norm_emerged',
      actor: 'system',
      description: `Norm "${norm.name}" emerged in ${norm.domain} domain`,
      impact: norm.strength * 0.1,
      metadata: { normId: norm.id, normName: norm.name, domain: norm.domain }
    });

    this.emit('norm_emerged', norm);
    return norm.id;
  }

  public enforceNorm(normId: string, context: Record<string, any>): boolean {
    const norm = this.norms.get(normId);
    if (!norm) return false;

    // Strengthen norm through enforcement
    norm.adoptionRate = Math.min(1, norm.adoptionRate + 0.02);
    norm.strength = Math.min(1, norm.strength + 0.01);

    this.recordEvent({
      type: 'norm_enforced',
      actor: 'system',
      description: `Norm "${norm.name}" enforced`,
      impact: norm.strength * 0.05,
      metadata: { normId, adoptionRate: norm.adoptionRate }
    });

    return true;
  }

  private pruneNorms(): void {
    const weakNorms = Array.from(this.norms.values())
      .filter(n => n.strength < 0.3 && n.adoptionRate < 0.3)
      .sort((a, b) => a.strength - b.strength);

    // Remove weakest norm
    if (weakNorms.length > 0) {
      this.norms.delete(weakNorms[0].id);
    }
  }

  // ==========================================================================
  // Role Management
  // ==========================================================================

  public createRole(roleData: Omit<Role, 'id' | 'emergenceTime'>): string {
    if (this.roles.size >= this.MAX_ROLES) {
      return '';
    }

    const role: Role = {
      ...roleData,
      id: `role_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      emergenceTime: Date.now()
    };

    this.roles.set(role.id, role);
    this.recordEvent({
      type: 'role_created',
      actor: 'system',
      description: `Role "${role.name}" created in ${role.domain} domain`,
      impact: role.population * 0.01,
      metadata: { roleId: role.id, roleName: role.name, domain: role.domain }
    });

    this.emit('role_created', role);
    return role.id;
  }

  public specializeRole(roleId: string, specialization: string): boolean {
    const role = this.roles.get(roleId);
    if (!role) return false;

    if (!role.capabilities.includes(specialization)) {
      role.capabilities.push(specialization);
      role.specialization = Math.min(1, role.specialization + 0.05);
    }

    this.recordEvent({
      type: 'role_specialized',
      actor: 'system',
      description: `Role "${role.name}" specialized in ${specialization}`,
      impact: 0.02,
      metadata: { roleId, specialization }
    });

    return true;
  }

  // ==========================================================================
  // Institution Management
  // ==========================================================================

  public formInstitution(institutionData: Omit<Institution, 'id' | 'createdAt'>): string {
    if (this.institutions.size >= this.MAX_INSTITUTIONS) {
      return '';
    }

    const institution: Institution = {
      ...institutionData,
      id: `inst_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      createdAt: Date.now()
    };

    this.institutions.set(institution.id, institution);
    this.recordEvent({
      type: 'institution_formed',
      actor: 'system',
      description: `Institution "${institution.name}" formed as ${institution.type}`,
      impact: institution.authority * 0.1,
      metadata: { institutionId: institution.id, institutionName: institution.name, type: institution.type }
    });

    this.emit('institution_formed', institution);
    return institution.id;
  }

  // ==========================================================================
  // Governance Evolution
  // ==========================================================================

  private startEvolutionCycle(): void {
    // Run evolution cycle every 60 seconds
    setInterval(() => {
      this.evolutionCycles++;
      this.evolveGovernance();
    }, 60000);
  }

  private evolveGovernance(): void {
    // Evolve laws
    this.evolveLaws();

    // Evolve norms
    this.evolveNorms();

    // Evolve roles
    this.evolveRoles();

    // Update metrics
    this.updateMetrics();

    this.emit('governance_evolved', {
      cycle: this.evolutionCycles,
      laws: this.laws.size,
      norms: this.norms.size,
      roles: this.roles.size,
      institutions: this.institutions.size,
      effectiveness: this.governanceEffectiveness,
      cultureScore: this.cultureScore
    });
  }

  private evolveNorms(): void {
    // Strengthen adopted norms, weaken unused norms
    this.norms.forEach(norm => {
      if (norm.adoptionRate > 0.7) {
        norm.strength = Math.min(1, norm.strength + 0.01);
      } else if (norm.adoptionRate < 0.3) {
        norm.strength = Math.max(0, norm.strength - 0.02);
      }
    });
  }

  private evolveRoles(): void {
    // Evolve role specializations based on performance
    this.roles.forEach(role => {
      if (role.performance > 0.8) {
        role.specialization = Math.min(1, role.specialization + 0.01);
      }
    });
  }

  private updateMetrics(): void {
    // Calculate governance effectiveness
    const lawEffectiveness = Array.from(this.laws.values()).reduce((sum, law) => sum + law.effectiveness, 0) / this.laws.size;
    const normAdoption = Array.from(this.norms.values()).reduce((sum, norm) => sum + norm.adoptionRate, 0) / this.norms.size;
    const rolePerformance = Array.from(this.roles.values()).reduce((sum, role) => sum + role.performance, 0) / this.roles.size;

    this.governanceEffectiveness = (lawEffectiveness * 0.4) + (normAdoption * 0.3) + (rolePerformance * 0.3);
    this.cultureScore = normAdoption * 0.8 + this.governanceEffectiveness * 0.2;
  }

  // ==========================================================================
  // Event Management
  // ==========================================================================

  private recordEvent(event: Omit<GovernanceEvent, 'id' | 'timestamp'>): void {
    const fullEvent: GovernanceEvent = {
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
  // Utility Methods
  // ==========================================================================

  private getSeverityImpact(severity: Law['severity']): number {
    switch (severity) {
      case 'critical': return 1;
      case 'mandatory': return 0.6;
      case 'guideline': return 0.3;
    }
  }

  // ==========================================================================
  // Public API
  // ==========================================================================

  public getState(): GovernanceState {
    return {
      laws: Array.from(this.laws.values()),
      norms: Array.from(this.norms.values()),
      roles: Array.from(this.roles.values()),
      institutions: Array.from(this.institutions.values()),
      cultureScore: this.cultureScore,
      governanceEffectiveness: this.governanceEffectiveness
    };
  }

  public getLaws(): Law[] {
    return Array.from(this.laws.values());
  }

  public getNorms(): Norm[] {
    return Array.from(this.norms.values());
  }

  public getRoles(): Role[] {
    return Array.from(this.roles.values());
  }

  public getInstitutions(): Institution[] {
    return Array.from(this.institutions.values());
  }

  public getEvents(limit?: number): GovernanceEvent[] {
    return limit ? this.events.slice(-limit) : this.events;
  }

  public getStatistics(): {
    laws: number;
    norms: number;
    roles: number;
    institutions: number;
    events: number;
    evolutionCycles: number;
    governanceEffectiveness: number;
    cultureScore: number;
  } {
    return {
      laws: this.laws.size,
      norms: this.norms.size,
      roles: this.roles.size,
      institutions: this.institutions.size,
      events: this.events.length,
      evolutionCycles: this.evolutionCycles,
      governanceEffectiveness: this.governanceEffectiveness,
      cultureScore: this.cultureScore
    };
  }
}