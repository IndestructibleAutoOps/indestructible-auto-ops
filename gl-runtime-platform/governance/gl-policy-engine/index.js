// @GL-governed
// GL-ROOT Global Governance Audit & Platform Build
// Unified Charter v2.0.0 - GL Policy Engine

const fs = require('fs').promises;
const path = require('path');
const { v4: uuidv4 } = require('uuid');
const winston = require('winston');
const yaml = require('js-yaml');

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.json(),
  transports: [
    new winston.transports.File({ filename: '../../storage/gl-events-stream/gl-policy-engine.log' }),
    new winston.transports.Console()
  ]
});

class GLPolicyEngine {
  constructor() {
    this.policies = new Map();
    this.schemas = new Map();
    this.eventStream = [];
    this.loadPolicies();
    this.loadSchemas();
  }

  async loadPolicies() {
    try {
      const policiesPath = path.join(__dirname, 'policies.yaml');
      const content = await fs.readFile(policiesPath, 'utf8');
      const policies = yaml.load(content);
      
      policies.forEach(policy => {
        this.policies.set(policy.id, policy);
      });
      
      logger.info('Policies loaded', { count: this.policies.size });
      this.logEvent('policies_loaded', { count: this.policies.size });
    } catch (error) {
      logger.warn('Policies not found, using defaults', { error: error.message });
      this.initializeDefaultPolicies();
    }
  }

  async loadSchemas() {
    try {
      const schemasPath = path.join(__dirname, 'schemas.yaml');
      const content = await fs.readFile(schemasPath, 'utf8');
      const schemas = yaml.load(content);
      
      schemas.forEach(schema => {
        this.schemas.set(schema.id, schema);
      });
      
      logger.info('Schemas loaded', { count: this.schemas.size });
      this.logEvent('schemas_loaded', { count: this.schemas.size });
    } catch (error) {
      logger.warn('Schemas not found, using defaults', { error: error.message });
      this.initializeDefaultSchemas();
    }
  }

  initializeDefaultPolicies() {
    const defaultPolicies = [
      {
        id: 'policy-schema-validation',
        name: 'Schema Validation Policy',
        type: 'validation',
        scope: 'configuration',
        description: 'All configuration files must conform to their schemas',
        enforcement: 'strict',
        rules: [
          'yaml_syntax',
          'json_syntax',
          'schema_compliance'
        ]
      },
      {
        id: 'policy-naming-convention',
        name: 'Naming Convention Policy',
        type: 'naming',
        scope: 'all',
        description: 'All entities must follow GL naming conventions',
        enforcement: 'moderate',
        rules: [
          'lowercase_files',
          'gl_prefix_special',
          'kebab_case_directories'
        ]
      },
      {
        id: 'policy-path-structure',
        name: 'Path Structure Policy',
        type: 'structure',
        scope: 'filesystem',
        description: 'Directory structure must follow GL hierarchy',
        enforcement: 'strict',
        rules: [
          'layer_separation',
          'module_isolation',
          'clear_separation_of_concerns'
        ]
      },
      {
        id: 'policy-governance-compliance',
        name: 'Governance Compliance Policy',
        type: 'governance',
        scope: 'all',
        description: 'All artifacts must include required governance metadata',
        enforcement: 'strict',
        rules: [
          'gl_governed_marker',
          'semantic_anchoring',
          'audit_trail_inclusion'
        ]
      }
    ];

    defaultPolicies.forEach(policy => {
      this.policies.set(policy.id, policy);
    });

    logger.info('Default policies initialized', { count: defaultPolicies.length });
    this.logEvent('default_policies_initialized', { count: defaultPolicies.length });
  }

  initializeDefaultSchemas() {
    const defaultSchemas = [
      {
        id: 'schema-yaml-config',
        type: 'yaml',
        description: 'YAML configuration schema',
        required_fields: ['apiVersion', 'kind', 'metadata', 'spec'],
        optional_fields: ['status', 'annotations']
      },
      {
        id: 'schema-json-governance',
        type: 'json',
        description: 'Governance artifact schema',
        required_fields: ['id', 'timestamp', 'type', 'data', 'source'],
        optional_fields: ['metadata', 'severity']
      },
      {
        id: 'schema-pipeline-execution',
        type: 'yaml',
        description: 'Pipeline execution schema',
        required_fields: ['name', 'stages', 'triggers'],
        optional_fields: ['parameters', 'environment', 'hooks']
      }
    ];

    defaultSchemas.forEach(schema => {
      this.schemas.set(schema.id, schema);
    });

    logger.info('Default schemas initialized', { count: defaultSchemas.length });
    this.logEvent('default_schemas_initialized', { count: defaultSchemas.length });
  }

  async validateAgainstSchema(file, schemaId) {
    const schema = this.schemas.get(schemaId);
    if (!schema) {
      throw new Error(`Schema not found: ${schemaId}`);
    }

    const content = await fs.readFile(file, 'utf8');
    let data;
    
    try {
      if (schema.type === 'yaml') {
        data = yaml.load(content);
      } else if (schema.type === 'json') {
        data = JSON.parse(content);
      } else {
        throw new Error(`Unsupported schema type: ${schema.type}`);
      }
    } catch (error) {
      return {
        valid: false,
        errors: [`Parse error: ${error.message}`]
      };
    }

    const errors = [];
    
    // Check required fields
    schema.required_fields.forEach(field => {
      if (!data[field]) {
        errors.push(`Missing required field: ${field}`);
      }
    });

    const result = {
      valid: errors.length === 0,
      schema: schemaId,
      file,
      errors,
      warnings: []
    };

    this.logEvent('schema_validation', result);
    return result;
  }

  async validateNamingConvention(entity, entityType) {
    const violations = [];

    // Check lowercase rule
    if (/[A-Z]/.test(entity)) {
      violations.push({
        rule: 'lowercase_files',
        severity: 'warning',
        message: 'Contains uppercase characters'
      });
    }

    // Check GL prefix for special entities
    if (entityType === 'special' && !entity.startsWith('gl-') && !entity.startsWith('GL-')) {
      violations.push({
        rule: 'gl_prefix_special',
        severity: 'error',
        message: 'Special entities must have gl- or GL- prefix'
      });
    }

    // Check kebab-case for directories
    if (entityType === 'directory' && /[^a-z0-9-]/.test(entity)) {
      violations.push({
        rule: 'kebab_case_directories',
        severity: 'error',
        message: 'Directories must be kebab-case'
      });
    }

    const result = {
      valid: violations.filter(v => v.severity === 'error').length === 0,
      entity,
      entityType,
      violations
    };

    this.logEvent('naming_validation', result);
    return result;
  }

  async validatePathStructure(filePath) {
    const violations = [];
    const parts = filePath.split(path.sep);

    // Check layer separation
    const layerPattern = /^(gl|GL)[0-9]+-[0-9]+$/;
    const hasLayer = parts.some(part => layerPattern.test(part));
    
    if (!hasLayer && parts.includes('governance')) {
      violations.push({
        rule: 'layer_separation',
        severity: 'warning',
        message: 'Governance files should be within GL layers'
      });
    }

    // Check module isolation
    if (parts.includes('engine') && parts.includes('connectors')) {
      violations.push({
        rule: 'module_isolation',
        severity: 'error',
        message: 'Mixing engine and connectors in same path'
      });
    }

    const result = {
      valid: violations.filter(v => v.severity === 'error').length === 0,
      path: filePath,
      violations
    };

    this.logEvent('path_validation', result);
    return result;
  }

  async validateGovernanceCompliance(file) {
    const violations = [];
    
    try {
      const content = await fs.readFile(file, 'utf8');
      
      // Check GL governed marker
      if (!content.includes('@GL-governed')) {
        violations.push({
          rule: 'gl_governed_marker',
          severity: 'error',
          message: 'Missing @GL-governed marker'
        });
      }

      // Check semantic anchoring
      if (!content.includes('@GL-semantic')) {
        violations.push({
          rule: 'semantic_anchoring',
          severity: 'warning',
          message: 'Missing @GL-semantic anchor'
        });
      }

      // Check audit trail inclusion
      if (!content.includes('@GL-audit-trail')) {
        violations.push({
          rule: 'audit_trail_inclusion',
          severity: 'info',
          message: 'Missing @GL-audit-trail reference'
        });
      }
    } catch (error) {
      violations.push({
        rule: 'file_read',
        severity: 'error',
        message: `Cannot read file: ${error.message}`
      });
    }

    const result = {
      valid: violations.filter(v => v.severity === 'error').length === 0,
      file,
      violations
    };

    this.logEvent('governance_compliance', result);
    return result;
  }

  getPolicies() {
    return Array.from(this.policies.values());
  }

  getSchemas() {
    return Array.from(this.schemas.values());
  }

  logEvent(type, data) {
    const event = {
      id: uuidv4(),
      timestamp: new Date().toISOString(),
      type,
      data,
      source: 'gl-policy-engine'
    };
    this.eventStream.push(event);
    logger.info('GL Policy Engine event logged', event);

    fs.appendFile(
      path.join(__dirname, '../../storage/gl-events-stream/gl-policy-events.jsonl'),
      JSON.stringify(event) + '\n'
    ).catch(err => logger.error('Event stream write failed', { error: err.message }));
  }
}

module.exports = GLPolicyEngine;