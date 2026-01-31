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
 * Module: Ecosystem Formation Engine
 * 
 * The ecosystem engine enables the formation of a balanced ecological system
 * with producers, consumers, repairers, optimizers, guardians, and explorers.
 * 
 * Key Capabilities:
 * - Ecological role management
 * - Resource flow tracking
 * - Ecosystem balance maintenance
 * - Population dynamics
 * - Inter-species relationships
 * - Ecological health monitoring
 */

import { EventEmitter } from 'events';

// ============================================================================
// Core Types
// ============================================================================

export interface EcologicalRole {
  id: string;
  name: string;
  type: 'producer' | 'consumer' | 'repairer' | 'optimizer' | 'guardian' | 'explorer';
  description: string;
  responsibilities: string[];
  population: number;
  productivity: number; // 0-1
  resourceConsumption: number; // 0-1
  resourceProduction: number; // 0-1
  efficiency: number; // 0-1
  health: number; // 0-1
  collaborationScore: number; // 0-1
  emergenceTime: number;
}

export interface Resource {
  id: string;
  name: string;
  type: 'strategy' | 'knowledge' | 'compute' | 'storage' | 'network' | 'semantic';
  totalAvailable: number;
  currentAvailable: number;
  productionRate: number;
  consumptionRate: number;
  lastUpdated: number;
}

export interface EcologicalRelationship {
  id: string;
  fromRole: string;
  toRole: string;
  type: 'symbiotic' | 'competitive' | 'cooperative' | 'dependent';
  strength: number; // 0-1
  benefitToFrom: number; // -1 to 1
  benefitToTo: number; // -1 to 1
  formationTime: number;
}

export interface EcosystemEvent {
  id: string;
  type: 'role_created' | 'population_changed' | 'resource_shift' | 
        'relationship_formed' | 'imbalance_detected' | 'balance_restored';
  timestamp: number;
  description: string;
  severity: 'info' | 'warning' | 'critical';
  impact: number; // -1 to 1
  metadata: Record<string, any>;
}

export interface EcosystemHealth {
  overall: number; // 0-1
  balance: number; // 0-1
  diversity: number; // 0-1
  stability: number; // 0-1
  productivity: number; // 0-1
}

export interface EcosystemState {
  roles: EcologicalRole[];
  resources: Resource[];
  relationships: EcologicalRelationship[];
  health: EcosystemHealth;
  totalPopulation: number;
  dominantRoleType: string;
}

// ============================================================================
// Main Ecosystem Engine Class
// ============================================================================

export class EcosystemEngine extends EventEmitter {
  private roles: Map<string, EcologicalRole> = new Map();
  private resources: Map<string, Resource> = new Map();
  private relationships: Map<string, EcologicalRelationship> = new Map();
  private events: EcosystemEvent[] = [];
  
  // Configuration
  private readonly MAX_ROLES = 50;
  private readonly MAX_RESOURCES = 20;
  private readonly MAX_RELATIONSHIPS = 100;
  private readonly EVENT_RETENTION_DAYS = 365;
  private readonly HEALTH_CHECK_INTERVAL = 30000; // 30 seconds
  
  // Metrics
  private health: EcosystemHealth = {
    overall: 0.5,
    balance: 0.5,
    diversity: 0.5,
    stability: 0.5,
    productivity: 0.5
  };
  private evolutionCycles: number = 0;

  constructor() {
    super();
    this.initializeEcosystem();
  }

  // ==========================================================================
  // Initialization
  // ==========================================================================

  private initializeEcosystem(): void {
    // Define resources
    this.defineResources();
    
    // Create ecological roles
    this.createEcologicalRoles();
    
    // Establish relationships
    this.establishRelationships();
    
    // Start monitoring
    this.startHealthMonitoring();
    
    this.emit('ecosystem_initialized', {
      roles: this.roles.size,
      resources: this.resources.size,
      relationships: this.relationships.size
    });
  }

  private defineResources(): void {
    const resources: Omit<Resource, 'id' | 'lastUpdated'>[] = [
      {
        name: 'Strategies',
        type: 'strategy',
        totalAvailable: 1000,
        currentAvailable: 800,
        productionRate: 10,
        consumptionRate: 8
      },
      {
        name: 'Knowledge',
        type: 'knowledge',
        totalAvailable: 5000,
        currentAvailable: 4500,
        productionRate: 50,
        consumptionRate: 40
      },
      {
        name: 'Compute',
        type: 'compute',
        totalAvailable: 100,
        currentAvailable: 70,
        productionRate: 5,
        consumptionRate: 8
      },
      {
        name: 'Storage',
        type: 'storage',
        totalAvailable: 10000,
        currentAvailable: 8500,
        productionRate: 100,
        consumptionRate: 80
      },
      {
        name: 'Network',
        type: 'network',
        totalAvailable: 1000,
        currentAvailable: 900,
        productionRate: 20,
        consumptionRate: 18
      },
      {
        name: 'Semantic',
        type: 'semantic',
        totalAvailable: 2000,
        currentAvailable: 1800,
        productionRate: 15,
        consumptionRate: 12
      }
    ];

    resources.forEach(resource => {
      this.resources.set(
        `res_${resource.name.toLowerCase()}`,
        { ...resource, id: `res_${resource.name.toLowerCase()}`, lastUpdated: Date.now() }
      );
    });
  }

  private createEcologicalRoles(): void {
    const ecologicalRoles: Omit<EcologicalRole, 'id' | 'emergenceTime'>[] = [
      {
        name: 'Strategy Producers',
        type: 'producer',
        description: 'Generate new strategies and solutions for the civilization',
        responsibilities: [
          'Generate novel strategies',
          'Create innovative solutions',
          'Explore new approaches',
          'Contribute to strategy repository'
        ],
        population: 10,
        productivity: 0.85,
        resourceConsumption: 0.6,
        resourceProduction: 0.9,
        efficiency: 0.82,
        health: 0.9,
        collaborationScore: 0.75
      },
      {
        name: 'Strategy Consumers',
        type: 'consumer',
        description: 'Execute strategies and consume resources',
        responsibilities: [
          'Execute strategies',
          'Consume resources efficiently',
          'Provide feedback on strategies',
          'Report execution results'
        ],
        population: 15,
        productivity: 0.88,
        resourceConsumption: 0.8,
        resourceProduction: 0.3,
        efficiency: 0.85,
        health: 0.92,
        collaborationScore: 0.8
      },
      {
        name: 'System Repairers',
        type: 'repairer',
        description: 'Repair and maintain the system infrastructure',
        responsibilities: [
          'Identify system issues',
          'Repair broken components',
          'Maintain system health',
          'Prevent failures'
        ],
        population: 8,
        productivity: 0.9,
        resourceConsumption: 0.5,
        resourceProduction: 0.4,
        efficiency: 0.88,
        health: 0.95,
        collaborationScore: 0.85
      },
      {
        name: 'System Optimizers',
        type: 'optimizer',
        description: 'Optimize system performance and efficiency',
        responsibilities: [
          'Analyze performance metrics',
          'Optimize execution paths',
          'Improve resource utilization',
          'Enhance system efficiency'
        ],
        population: 6,
        productivity: 0.87,
        resourceConsumption: 0.4,
        resourceProduction: 0.5,
        efficiency: 0.9,
        health: 0.93,
        collaborationScore: 0.82
      },
      {
        name: 'Civilization Guardians',
        type: 'guardian',
        description: 'Guard civilization values, norms, and integrity',
        responsibilities: [
          'Enforce governance rules',
          'Protect cultural values',
          'Maintain system integrity',
          'Ensure compliance'
        ],
        population: 5,
        productivity: 0.92,
        resourceConsumption: 0.3,
        resourceProduction: 0.2,
        efficiency: 0.95,
        health: 0.97,
        collaborationScore: 0.9
      },
      {
        name: 'Innovation Explorers',
        type: 'explorer',
        description: 'Explore new technologies, approaches, and possibilities',
        responsibilities: [
          'Explore new technologies',
          'Test innovative approaches',
          'Discover new possibilities',
          'Push boundaries'
        ],
        population: 7,
        productivity: 0.8,
        resourceConsumption: 0.7,
        resourceProduction: 0.6,
        efficiency: 0.78,
        health: 0.88,
        collaborationScore: 0.72
      }
    ];

    ecologicalRoles.forEach(role => {
      this.createRole(role);
    });
  }

  private establishRelationships(): void {
    const roleIds = Array.from(this.roles.keys());
    
    // Define symbiotic relationships
    const symbioticPairs = [
      ['producer', 'consumer'],
      ['repairer', 'optimizer'],
      ['guardian', 'producer'],
      ['explorer', 'optimizer']
    ];

    symbioticPairs.forEach(([type1, type2]) => {
      const roles1 = Array.from(this.roles.values()).filter(r => r.type === type1);
      const roles2 = Array.from(this.roles.values()).filter(r => r.type === type2);

      roles1.forEach(role1 => {
        roles2.forEach(role2 => {
          this.createRelationship({
            fromRole: role1.id,
            toRole: role2.id,
            type: 'symbiotic',
            strength: 0.7 + Math.random() * 0.2,
            benefitToFrom: 0.3,
            benefitToTo: 0.5
          });
        });
      });
    });

    // Define competitive relationships
    const competitivePairs = [
      ['producer', 'explorer'],
      ['consumer', 'optimizer']
    ];

    competitivePairs.forEach(([type1, type2]) => {
      const roles1 = Array.from(this.roles.values()).filter(r => r.type === type1);
      const roles2 = Array.from(this.roles.values()).filter(r => r.type === type2);

      roles1.forEach(role1 => {
        roles2.forEach(role2 => {
          if (Math.random() > 0.5) {
            this.createRelationship({
              fromRole: role1.id,
              toRole: role2.id,
              type: 'competitive',
              strength: 0.3 + Math.random() * 0.3,
              benefitToFrom: 0.1,
              benefitToTo: -0.1
            });
          }
        });
      });
    });
  }

  // ==========================================================================
  // Role Management
  // ==========================================================================

  public createRole(roleData: Omit<EcologicalRole, 'id' | 'emergenceTime'>): string {
    if (this.roles.size >= this.MAX_ROLES) {
      return '';
    }

    const role: EcologicalRole = {
      ...roleData,
      id: `role_${roleData.name.toLowerCase().replace(/\s+/g, '_')}_${Date.now()}`,
      emergenceTime: Date.now()
    };

    this.roles.set(role.id, role);
    this.recordEvent({
      type: 'role_created',
      description: `Ecological role "${role.name}" created as ${role.type}`,
      severity: 'info',
      impact: 0.1,
      metadata: { roleId: role.id, type: role.type, population: role.population }
    });

    this.emit('role_created', role);
    return role.id;
  }

  public adjustPopulation(roleId: string, change: number): boolean {
    const role = this.roles.get(roleId);
    if (!role) return false;

    const oldPopulation = role.population;
    role.population = Math.max(1, role.population + change);
    
    this.recordEvent({
      type: 'population_changed',
      description: `Role "${role.name}" population changed from ${oldPopulation} to ${role.population}`,
      severity: Math.abs(change) > 5 ? 'warning' : 'info',
      impact: change * 0.01,
      metadata: { roleId, oldPopulation, newPopulation: role.population }
    });

    this.emit('population_changed', role);
    return true;
  }

  // ==========================================================================
  // Resource Management
  // ==========================================================================

  public updateResources(): void {
    this.resources.forEach(resource => {
      // Apply production and consumption
      resource.currentAvailable = Math.min(
        resource.totalAvailable,
        Math.max(0, resource.currentAvailable + resource.productionRate - resource.consumptionRate)
      );
      resource.lastUpdated = Date.now();

      // Emit warning if resource is low
      if (resource.currentAvailable < resource.totalAvailable * 0.2) {
        this.recordEvent({
          type: 'resource_shift',
          description: `Resource "${resource.name}" is low: ${resource.currentAvailable}/${resource.totalAvailable}`,
          severity: 'warning',
          impact: -0.1,
          metadata: { resourceId: resource.id, currentAvailable: resource.currentAvailable, totalAvailable: resource.totalAvailable }
        });
      }
    });
  }

  // ==========================================================================
  // Relationship Management
  // ==========================================================================

  public createRelationship(relationshipData: Omit<EcologicalRelationship, 'id' | 'formationTime'>): string {
    if (this.relationships.size >= this.MAX_RELATIONSHIPS) {
      return '';
    }

    const relationship: EcologicalRelationship = {
      ...relationshipData,
      id: `rel_${relationshipData.fromRole}_${relationshipData.toRole}_${Date.now()}`,
      formationTime: Date.now()
    };

    this.relationships.set(relationship.id, relationship);
    this.recordEvent({
      type: 'relationship_formed',
      description: `Relationship formed between ${relationshipData.fromRole} and ${relationshipData.toRole}`,
      severity: 'info',
      impact: relationship.strength * 0.05,
      metadata: { relationshipId: relationship.id, type: relationship.type, strength: relationship.strength }
    });

    return relationship.id;
  }

  // ==========================================================================
  // Ecosystem Health Monitoring
  // ==========================================================================

  private startHealthMonitoring(): void {
    setInterval(() => {
      this.evolutionCycles++;
      this.monitorEcosystem();
    }, this.HEALTH_CHECK_INTERVAL);
  }

  private monitorEcosystem(): void {
    // Update resources
    this.updateResources();

    // Calculate health metrics
    this.calculateHealth();

    // Check for imbalances
    this.checkImbalances();

    // Auto-balance if needed
    this.autoBalance();

    this.emit('ecosystem_monitored', {
      cycle: this.evolutionCycles,
      health: this.health,
      roles: this.roles.size,
      resources: this.resources.size
    });
  }

  private calculateHealth(): void {
    // Calculate balance (distribution of role types)
    const roleTypes = new Map<string, number>();
    this.roles.forEach(role => {
      const count = roleTypes.get(role.type) || 0;
      roleTypes.set(role.type, count + role.population);
    });

    const populations = Array.from(roleTypes.values());
    const totalPopulation = populations.reduce((sum, pop) => sum + pop, 0);
    const avgPopulation = totalPopulation / populations.length;
    const variance = populations.reduce((sum, pop) => sum + Math.pow(pop - avgPopulation, 2), 0) / populations.length;
    this.health.balance = Math.max(0, 1 - (variance / (avgPopulation * avgPopulation)));

    // Calculate diversity (Shannon diversity index)
    const diversity = populations.reduce((sum, pop) => {
      const p = pop / totalPopulation;
      return sum - (p * Math.log2(p));
    }, 0);
    const maxDiversity = Math.log2(populations.length);
    this.health.diversity = diversity / maxDiversity;

    // Calculate stability (role health average)
    const avgRoleHealth = Array.from(this.roles.values())
      .reduce((sum, role) => sum + role.health, 0) / this.roles.size;
    this.health.stability = avgRoleHealth;

    // Calculate productivity (role productivity average)
    const avgProductivity = Array.from(this.roles.values())
      .reduce((sum, role) => sum + role.productivity, 0) / this.roles.size;
    this.health.productivity = avgProductivity;

    // Calculate overall health
    this.health.overall = (
      this.health.balance * 0.25 +
      this.health.diversity * 0.2 +
      this.health.stability * 0.25 +
      this.health.productivity * 0.3
    );
  }

  private checkImbalances(): void {
    // Check if any role type is underrepresented
    const roleTypes = new Map<string, number>();
    this.roles.forEach(role => {
      const count = roleTypes.get(role.type) || 0;
      roleTypes.set(role.type, count + role.population);
    });

    const totalPopulation = Array.from(roleTypes.values()).reduce((sum, pop) => sum + pop, 0);
    const avgPopulation = totalPopulation / roleTypes.size;

    roleTypes.forEach((population, type) => {
      if (population < avgPopulation * 0.5) {
        this.recordEvent({
          type: 'imbalance_detected',
          description: `Role type "${type}" is underrepresented: ${population} vs avg ${avgPopulation}`,
          severity: 'warning',
          impact: -0.1,
          metadata: { type, population, avgPopulation }
        });
      }
    });

    // Check if resources are depleted
    this.resources.forEach(resource => {
      if (resource.currentAvailable < resource.totalAvailable * 0.1) {
        this.recordEvent({
          type: 'imbalance_detected',
          description: `Resource "${resource.name}" is critically low: ${resource.currentAvailable}/${resource.totalAvailable}`,
          severity: 'critical',
          impact: -0.2,
          metadata: { resourceId: resource.id, currentAvailable: resource.currentAvailable }
        });
      }
    });
  }

  private autoBalance(): void {
    // Adjust populations to maintain balance
    const roleTypes = new Map<string, number>();
    this.roles.forEach(role => {
      const count = roleTypes.get(role.type) || 0;
      roleTypes.set(role.type, count + role.population);
    });

    const totalPopulation = Array.from(roleTypes.values()).reduce((sum, pop) => sum + pop, 0);
    const avgPopulation = totalPopulation / roleTypes.size;

    this.roles.forEach(role => {
      const typePopulation = roleTypes.get(role.type) || 0;
      if (typePopulation < avgPopulation * 0.6) {
        // Increase population
        this.adjustPopulation(role.id, 1);
      } else if (typePopulation > avgPopulation * 1.4) {
        // Decrease population
        this.adjustPopulation(role.id, -1);
      }
    });
  }

  // ==========================================================================
  // Event Management
  // ==========================================================================

  private recordEvent(event: Omit<EcosystemEvent, 'id' | 'timestamp'>): void {
    const fullEvent: EcosystemEvent = {
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

  public getState(): EcosystemState {
    const totalPopulation = Array.from(this.roles.values())
      .reduce((sum, role) => sum + role.population, 0);

    const dominantType = Array.from(this.roles.values())
      .reduce((max, role) => role.population > max.population ? role : max, { type: '', population: 0 });

    return {
      roles: Array.from(this.roles.values()),
      resources: Array.from(this.resources.values()),
      relationships: Array.from(this.relationships.values()),
      health: this.health,
      totalPopulation,
      dominantRoleType: dominantType.type
    };
  }

  public getRoles(): EcologicalRole[] {
    return Array.from(this.roles.values());
  }

  public getResources(): Resource[] {
    return Array.from(this.resources.values());
  }

  public getRelationships(): EcologicalRelationship[] {
    return Array.from(this.relationships.values());
  }

  public getEvents(limit?: number): EcosystemEvent[] {
    return limit ? this.events.slice(-limit) : this.events;
  }

  public getStatistics(): {
    roles: number;
    resources: number;
    relationships: number;
    events: number;
    totalPopulation: number;
    health: EcosystemHealth;
    evolutionCycles: number;
  } {
    const totalPopulation = Array.from(this.roles.values())
      .reduce((sum, role) => sum + role.population, 0);

    return {
      roles: this.roles.size,
      resources: this.resources.size,
      relationships: this.relationships.size,
      events: this.events.length,
      totalPopulation,
      health: this.health,
      evolutionCycles: this.evolutionCycles
    };
  }
}