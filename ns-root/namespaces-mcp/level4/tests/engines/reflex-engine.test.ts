// @GL-governed
// @GL-layer: GL-L6-NAMESPACE
// @GL-semantic: governance-layer-namespace
// @GL-revision: 1.0.0
// @GL-status: active

/**
 * GL Governance Markers
 * @gl-layer GL-00-NAMESPACE
 * @gl-module ns-root/namespaces-mcp/level4/tests/engines
 * @gl-semantic-anchor GL-00-TESTS_ENGINES_REFLEXENGINE
 * @gl-evidence-required false
 * GL Unified Charter Activated
 */

/**
 * Reflex Engine Unit Tests
 */

import { ReflexEngine } from '../../src/engines/reflex-engine';
import { IReflexConfig, EngineStatus, AutonomyLevel } from '../../src/interfaces';

describe('ReflexEngine', () => {
  let engine: ReflexEngine;
  let config: IReflexConfig;
  
  beforeEach(() => {
    config = {
      id: 'test-reflex-engine',
      name: 'Test Reflex Engine',
      version: '1.0.0',
      autonomyLevel: AutonomyLevel.HIGH,
      enabled: true,
      intervalMs: 60000,
      timeoutMs: 30000,
      maxRetries: 3,
      retryBackoff: 'exponential',
      config: {
        detectionIntervalMs: 10000,
        enableAutoRecovery: true,
        maxConcurrentRecoveries: 3
      },
      dependencies: [],
      tags: ['reflex', 'recovery']
    };
    
    engine = new ReflexEngine(config);
  });
  
  afterEach(async () => {
    if (engine.status === EngineStatus.RUNNING) {
      await engine.stop();
    }
  });
  
  describe('Initialization', () => {
    it('should initialize correctly', async () => {
      await engine.initialize();
      expect(engine.status).toBe(EngineStatus.IDLE);
    });
  });
  
  describe('Lifecycle', () => {
    it('should start and stop', async () => {
      await engine.initialize();
      await engine.start();
      expect(engine.status).toBe(EngineStatus.RUNNING);
      await engine.stop();
      expect(engine.status).toBe(EngineStatus.TERMINATED);
    });
  });
  
  describe('Fault Detection', () => {
    it('should detect faults', async () => {
      await engine.initialize();
      const faults = await engine.detectFaults();
      expect(Array.isArray(faults)).toBe(true);
    });
  });
  
  describe('Recovery', () => {
    it('should generate and execute recovery plan', async () => {
      await engine.initialize();
      const faults = await engine.detectFaults();
      
      if (faults.length > 0) {
        const planId = await engine.generateRecoveryPlan(faults[0].id);
        expect(planId).toBeDefined();
        
        const result = await engine.executeRecoveryPlan(planId);
        expect(result.success).toBe(true);
      }
    });
  });
  
  describe('Execution', () => {
    it('should execute successfully', async () => {
      await engine.initialize();
      const context = {
        executionId: 'test-exec-1',
        startedAt: new Date(),
        trigger: 'manual' as const,
        priority: 'medium' as const,
        metadata: {}
      };
      
      const result = await engine.execute(context);
      expect(result.success).toBe(true);
    });
  });
});