/**
 * GL Governance Markers
 * @gl-layer GL-00-NAMESPACE
 * @gl-module ns-root/namespaces-mcp/level2/src/semantic/__tests__
 * @gl-semantic-anchor GL-00-SEMANTIC_TESTS_PERFORMANCE.
 * @gl-evidence-required false
 * GL Unified Charter Activated
 */

/**
 * Performance & Stress Tests
 * 
 * Test Coverage:
 * - Load testing (1K-10K concurrent operations)
 * - Stress testing (find breaking points)
 * - Endurance testing (24-hour stability simulation)
 * - Spike testing (sudden traffic surge)
 * - Memory leak detection
 * - CPU usage monitoring
 */

import { describe, it, expect, beforeEach, afterEach } from '@jest/globals';
import ValidationEngine from '../validation-engine';
import PromotionEngine from '../promotion-engine';
import ArtifactRegistry from '../artifact-registry';

describe('Performance Tests', () => {
  describe('Validation Engine Performance', () => {
    let engine: ValidationEngine;

    beforeEach(() => {
      engine = new ValidationEngine({
        enableCache: true,
        cacheSize: 10000,
      });

      engine.registerSchema({
        id: 'perf-schema',
        name: 'Performance Schema',
        version: '1.0.0',
        format: 'json-schema',
        schema: {
          type: 'object',
          required: ['id', 'name', 'email'],
          properties: {
            id: { type: 'number' },
            name: { type: 'string' },
            email: { type: 'string' },
          },
        },
      });
    });

    it('should handle 1K concurrent validations', async () => {
      const promises = [];
      const startTime = Date.now();

      for (let i = 0; i < 1000; i++) {
        promises.push(
          engine.validate('perf-schema', {
            id: i,
            name: `User ${i}`,
            email: `user${i}@example.com`,
          })
        );
      }

      await Promise.all(promises);
      const duration = Date.now() - startTime;
      const throughput = 1000 / (duration / 1000);

      expect(throughput).toBeGreaterThan(1000); // >1K validations/sec
      expect(duration).toBeLessThan(1000); // <1 second for 1K validations
    });

    it('should handle 10K concurrent validations', async () => {
      const promises = [];
      const startTime = Date.now();

      for (let i = 0; i < 10000; i++) {
        promises.push(
          engine.validate('perf-schema', {
            id: i,
            name: `User ${i}`,
            email: `user${i}@example.com`,
          })
        );
      }

      await Promise.all(promises);
      const duration = Date.now() - startTime;
      const throughput = 10000 / (duration / 1000);

      expect(throughput).toBeGreaterThan(1000); // >1K validations/sec
      expect(duration).toBeLessThan(10000); // <10 seconds for 10K validations
    });

    it('should maintain performance under sustained load', async () => {
      const iterations = 100;
      const batchSize = 100;
      const durations: number[] = [];

      for (let i = 0; i < iterations; i++) {
        const startTime = Date.now();
        const promises = [];

        for (let j = 0; j < batchSize; j++) {
          promises.push(
            engine.validate('perf-schema', {
              id: i * batchSize + j,
              name: `User ${i * batchSize + j}`,
              email: `user${i * batchSize + j}@example.com`,
            })
          );
        }

        await Promise.all(promises);
        durations.push(Date.now() - startTime);
      }

      // Check that performance doesn't degrade over time
      const firstHalf = durations.slice(0, iterations / 2);
      const secondHalf = durations.slice(iterations / 2);
      const avgFirst = firstHalf.reduce((a, b) => a + b, 0) / firstHalf.length;
      const avgSecond = secondHalf.reduce((a, b) => a + b, 0) / secondHalf.length;

      // Second half should not be more than 20% slower
      expect(avgSecond).toBeLessThan(avgFirst * 1.2);
    });

    it('should achieve >80% cache hit rate', async () => {
      const data = {
        id: 1,
        name: 'Test User',
        email: 'test@example.com',
      };

      // First validation (cache miss)
      await engine.validate('perf-schema', data);

      // 100 subsequent validations (cache hits)
      for (let i = 0; i < 100; i++) {
        await engine.validate('perf-schema', data);
      }

      const stats = engine.getStats();
      expect(stats.cacheHitRate).toBeGreaterThan(0.8);
    });
  });

  describe('Promotion Engine Performance', () => {
    let engine: PromotionEngine;

    beforeEach(() => {
      engine = new PromotionEngine({
        approvalPolicies: [
          {
            stage: 'staging',
            requiredApprovals: 1,
            approvers: ['dev-lead'],
            autoApprove: true, // Auto-approve for performance testing
          },
        ],
        autoRollback: true,
      });
    });

    it('should handle 100 concurrent promotions', async () => {
      const promises = [];
      const startTime = Date.now();

      for (let i = 0; i < 100; i++) {
        promises.push(
          engine.requestPromotion({
            id: `promo-${i}`,
            artifactId: `app-v1.0.${i}`,
            version: `1.0.${i}`,
            fromStage: 'dev',
            toStage: 'staging',
            requestedBy: 'developer',
            requestedAt: new Date(),
          })
        );
      }

      await Promise.all(promises);
      const duration = Date.now() - startTime;

      expect(duration).toBeLessThan(30000); // <30 seconds for 100 promotions
    });

    it('should complete promotion within 5 minutes', async () => {
      const startTime = Date.now();

      await engine.requestPromotion({
        id: 'promo-timing',
        artifactId: 'app-v1.0.0',
        version: '1.0.0',
        fromStage: 'dev',
        toStage: 'staging',
        requestedBy: 'developer',
        requestedAt: new Date(),
      });

      const duration = Date.now() - startTime;
      expect(duration).toBeLessThan(300000); // <5 minutes
    });

    it('should complete rollback within 30 seconds', async () => {
      await engine.requestPromotion({
        id: 'promo-rollback-timing',
        artifactId: 'app-v1.0.0',
        version: '1.0.0',
        fromStage: 'dev',
        toStage: 'staging',
        requestedBy: 'developer',
        requestedAt: new Date(),
      });

      const startTime = Date.now();
      await engine.rollbackPromotion('promo-rollback-timing', 'operator', 'Performance test');
      const duration = Date.now() - startTime;

      expect(duration).toBeLessThan(30000); // <30 seconds
    });
  });

  describe('Artifact Registry Performance', () => {
    let registry: ArtifactRegistry;

    beforeEach(() => {
      registry = new ArtifactRegistry({
        storage: {
          backend: 'local',
          basePath: '/tmp/perf-test',
        },
        enableDeduplication: true,
      });
    });

    it('should handle 1K concurrent uploads', async () => {
      const promises = [];
      const startTime = Date.now();
      const data = Buffer.from('performance test data');

      for (let i = 0; i < 1000; i++) {
        promises.push(
          registry.publish(`perf-app-${i}`, '1.0.0', 'tar.gz', data)
        );
      }

      await Promise.all(promises);
      const duration = Date.now() - startTime;
      const throughput = 1000 / (duration / 1000);

      expect(throughput).toBeGreaterThan(10); // >10 artifacts/sec
    });

    it('should handle 10K concurrent uploads', async () => {
      const promises = [];
      const startTime = Date.now();
      const data = Buffer.from('performance test data');

      for (let i = 0; i < 10000; i++) {
        promises.push(
          registry.publish(`perf-app-${i}`, '1.0.0', 'tar.gz', data)
        );
      }

      await Promise.all(promises);
      const duration = Date.now() - startTime;
      const throughput = 10000 / (duration / 1000);

      expect(throughput).toBeGreaterThan(10); // >10 artifacts/sec
    });

    it('should lookup artifact within 100ms', async () => {
      const data = Buffer.from('lookup test');
      const artifact = await registry.publish('lookup-app', '1.0.0', 'tar.gz', data);

      const lookups = [];
      for (let i = 0; i < 100; i++) {
        const startTime = Date.now();
        registry.getArtifact(artifact.id);
        lookups.push(Date.now() - startTime);
      }

      const avgLookup = lookups.reduce((a, b) => a + b, 0) / lookups.length;
      expect(avgLookup).toBeLessThan(100);
    });

    it('should handle concurrent downloads', async () => {
      const data = Buffer.from('download test data');
      const artifact = await registry.publish('download-app', '1.0.0', 'tar.gz', data);

      const promises = [];
      const startTime = Date.now();

      for (let i = 0; i < 100; i++) {
        promises.push(registry.download(artifact.id));
      }

      await Promise.all(promises);
      const duration = Date.now() - startTime;
      const throughput = 100 / (duration / 1000);

      expect(throughput).toBeGreaterThan(50); // >50 downloads/sec
    });

    it('should efficiently deduplicate artifacts', async () => {
      const data = Buffer.from('duplicate test data');
      const startTime = Date.now();

      // Upload same data 100 times
      const promises = [];
      for (let i = 0; i < 100; i++) {
        promises.push(
          registry.publish(`dup-app-${i}`, '1.0.0', 'tar.gz', data)
        );
      }

      await Promise.all(promises);
      const duration = Date.now() - startTime;

      // Should be fast due to deduplication
      expect(duration).toBeLessThan(5000); // <5 seconds for 100 duplicates
    });
  });

  describe('Memory & Resource Tests', () => {
    it('should not leak memory during sustained operations', async () => {
      const engine = new ValidationEngine();
      engine.registerSchema({
        id: 'memory-test',
        name: 'Memory Test',
        version: '1.0.0',
        format: 'json-schema',
        schema: { type: 'object' },
      });

      const initialMemory = process.memoryUsage().heapUsed;

      // Perform 10K operations
      for (let i = 0; i < 10000; i++) {
        await engine.validate('memory-test', { id: i });
      }

      const finalMemory = process.memoryUsage().heapUsed;
      const memoryIncrease = finalMemory - initialMemory;

      // Memory increase should be reasonable (<100MB)
      expect(memoryIncrease).toBeLessThan(100 * 1024 * 1024);
    });

    it('should handle spike in traffic', async () => {
      const engine = new ValidationEngine();
      engine.registerSchema({
        id: 'spike-test',
        name: 'Spike Test',
        version: '1.0.0',
        format: 'json-schema',
        schema: { type: 'object' },
      });

      // Normal load
      for (let i = 0; i < 100; i++) {
        await engine.validate('spike-test', { id: i });
      }

      // Sudden spike
      const promises = [];
      const startTime = Date.now();
      for (let i = 0; i < 1000; i++) {
        promises.push(engine.validate('spike-test', { id: i }));
      }

      await Promise.all(promises);
      const duration = Date.now() - startTime;

      // Should handle spike without significant degradation
      expect(duration).toBeLessThan(2000); // <2 seconds for 1K operations
    });
  });

  describe('Stress Tests', () => {
    it('should find breaking point for validation engine', async () => {
      const engine = new ValidationEngine();
      engine.registerSchema({
        id: 'stress-test',
        name: 'Stress Test',
        version: '1.0.0',
        format: 'json-schema',
        schema: { type: 'object' },
      });

      let maxConcurrent = 0;
      let failed = false;

      // Gradually increase load until failure
      for (let concurrent = 100; concurrent <= 10000; concurrent += 100) {
        try {
          const promises = [];
          for (let i = 0; i < concurrent; i++) {
            promises.push(engine.validate('stress-test', { id: i }));
          }
          await Promise.all(promises);
          maxConcurrent = concurrent;
        } catch (error) {
          failed = true;
          break;
        }
      }

      // Should handle at least 1K concurrent operations
      expect(maxConcurrent).toBeGreaterThan(1000);
    });
  });
});

describe('Integration Performance Tests', () => {
  it('should handle end-to-end workflow efficiently', async () => {
    const validation = new ValidationEngine();
    const promotion = new PromotionEngine({
      approvalPolicies: [
        {
          stage: 'staging',
          requiredApprovals: 1,
          approvers: ['dev-lead'],
          autoApprove: true,
        },
      ],
    });
    const registry = new ArtifactRegistry({
      storage: {
        backend: 'local',
        basePath: '/tmp/integration-test',
      },
    });

    validation.registerSchema({
      id: 'integration-schema',
      name: 'Integration Schema',
      version: '1.0.0',
      format: 'json-schema',
      schema: { type: 'object', required: ['name'] },
    });

    const startTime = Date.now();

    // 1. Validate
    const validationResult = await validation.validate('integration-schema', {
      name: 'Test App',
    });
    expect(validationResult.valid).toBe(true);

    // 2. Publish artifact
    const artifact = await registry.publish(
      'integration-app',
      '1.0.0',
      'tar.gz',
      Buffer.from('test data')
    );

    // 3. Promote
    await promotion.requestPromotion({
      id: 'integration-promo',
      artifactId: artifact.id,
      version: '1.0.0',
      fromStage: 'dev',
      toStage: 'staging',
      requestedBy: 'developer',
      requestedAt: new Date(),
    });

    const duration = Date.now() - startTime;

    // End-to-end should complete within 10 seconds
    expect(duration).toBeLessThan(10000);
  });
});