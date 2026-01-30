// @GL-governed
// @GL-layer: GL90-99
// @GL-semantic: integration-test-suite
// @GL-charter-version: 4.0.0
// @GL-audit-trail: ../../engine/governance/GL_SEMANTIC_ANCHOR.json

/**
 * GL Runtime Platform - Integration Test Suite
 * Version 21.0.0
 * 
 * 測試跨組件整合：
 * - V19 Fabric ↔ Code Intelligence Layer
 * - V20 Continuum ↔ Code Intelligence Layer
 * - Pipeline ↔ Connector 整合
 * - 端到端工作流
 */

import { describe, test, expect, beforeEach, afterEach } from '@jest/globals';
import * as path from 'path';
import * as fs from 'fs';

// ============================================================================
// Test Results Tracking
// ============================================================================

interface TestResult {
  name: string;
  status: 'pass' | 'fail' | 'skip';
  duration: number;
  error?: string;
  details?: any;
}

interface IntegrationTestSuite {
  name: string;
  tests: TestResult[];
  startTime: number;
  endTime: number;
  status: 'pass' | 'fail' | 'partial';
}

// ============================================================================
// Utility Functions
// ============================================================================

function formatDuration(ms: number): string {
  if (ms < 1000) return `${ms}ms`;
  return `${(ms / 1000).toFixed(2)}s`;
}

function getTestDuration(startTime: number): number {
  return Date.now() - startTime;
}

// ============================================================================
// Integration Test Suite 1: V19 Fabric ↔ Code Intelligence Layer
// ============================================================================

describe('Integration Test Suite 1: V19 Fabric ↔ Code Intelligence Layer', () => {
  let suite: IntegrationTestSuite;
  const testResults: TestResult[] = [];

  beforeEach(() => {
    suite = {
      name: 'V19 Fabric ↔ Code Intelligence Layer',
      tests: [],
      startTime: Date.now(),
      endTime: 0,
      status: 'pass'
    };
  });

  afterEach(() => {
    suite.endTime = Date.now();
    suite.tests = testResults;
    suite.status = testResults.every(r => r.status === 'pass') ? 'pass' : 
                   testResults.some(r => r.status === 'pass') ? 'partial' : 'fail';
    
    console.log(`\n=== Suite Complete: ${suite.name} ===`);
    console.log(`Duration: ${formatDuration(suite.endTime - suite.startTime)}`);
    console.log(`Status: ${suite.status}`);
    console.log(`Tests: ${testResults.length}`);
  });

  test('1.1 Verify Fabric Continuum Integration file exists', async () => {
    const startTime = Date.now();
    try {
      const integrationPath = path.join(__dirname, '../../code-intelligence-security-layer/fabric-continuum-integration.ts');
      const exists = fs.existsSync(integrationPath);
      
      expect(exists).toBe(true);
      
      testResults.push({
        name: 'Verify Fabric Continuum Integration file exists',
        status: 'pass',
        duration: getTestDuration(startTime),
        details: { path: integrationPath }
      });
    } catch (error) {
      testResults.push({
        name: 'Verify Fabric Continuum Integration file exists',
        status: 'fail',
        duration: getTestDuration(startTime),
        error: error instanceof Error ? error.message : String(error)
      });
      throw error;
    }
  });

  test('1.2 Verify integration exports required classes', async () => {
    const startTime = Date.now();
    try {
      const integrationPath = path.join(__dirname, '../../code-intelligence-security-layer/index.ts');
      const content = fs.readFileSync(integrationPath, 'utf-8');
      
      const requiredExports = [
        'CapabilitySchemaRegistry',
        'PatternLibrary',
        'GeneratorEngine',
        'EvaluationEngine',
        'DeploymentWeaver',
        'EvolutionEngine'
      ];
      
      for (const exportName of requiredExports) {
        expect(content).toContain(`export ${exportName}`);
      }
      
      testResults.push({
        name: 'Verify integration exports required classes',
        status: 'pass',
        duration: getTestDuration(startTime),
        details: { exports: requiredExports }
      });
    } catch (error) {
      testResults.push({
        name: 'Verify integration exports required classes',
        status: 'fail',
        duration: getTestDuration(startTime),
        error: error instanceof Error ? error.message : String(error)
      });
      throw error;
    }
  });

  test('1.3 Verify Fabric Continuum Integration types', async () => {
    const startTime = Date.now();
    try {
      const integrationPath = path.join(__dirname, '../../code-intelligence-security-layer/fabric-continuum-integration.ts');
      const content = fs.readFileSync(integrationPath, 'utf-8');
      
      const requiredTypes = [
        'FabricContinuumIntegrationConfig',
        'IntegratedCapabilityRequest',
        'IntegratedCapabilityResponse',
        'FabricContinuumMetrics'
      ];
      
      for (const typeName of requiredTypes) {
        expect(content).toContain(`export interface ${typeName}`);
      }
      
      testResults.push({
        name: 'Verify Fabric Continuum Integration types',
        status: 'pass',
        duration: getTestDuration(startTime),
        details: { types: requiredTypes }
      });
    } catch (error) {
      testResults.push({
        name: 'Verify Fabric Continuum Integration types',
        status: 'fail',
        duration: getTestDuration(startTime),
        error: error instanceof Error ? error.message : String(error)
      });
      throw error;
    }
  });
});

// ============================================================================
// Integration Test Suite 2: V20 Continuum ↔ Code Intelligence Layer
// ============================================================================

describe('Integration Test Suite 2: V20 Continuum ↔ Code Intelligence Layer', () => {
  let suite: IntegrationTestSuite;
  const testResults: TestResult[] = [];

  beforeEach(() => {
    suite = {
      name: 'V20 Continuum ↔ Code Intelligence Layer',
      tests: [],
      startTime: Date.now(),
      endTime: 0,
      status: 'pass'
    };
  });

  afterEach(() => {
    suite.endTime = Date.now();
    suite.tests = testResults;
    suite.status = testResults.every(r => r.status === 'pass') ? 'pass' : 
                   testResults.some(r => r.status === 'pass') ? 'partial' : 'fail';
    
    console.log(`\n=== Suite Complete: ${suite.name} ===`);
    console.log(`Duration: ${formatDuration(suite.endTime - suite.startTime)}`);
    console.log(`Status: ${suite.status}`);
    console.log(`Tests: ${testResults.length}`);
  });

  test('2.1 Verify Infinite Continuum module structure', async () => {
    const startTime = Date.now();
    try {
      const continuumDir = path.join(__dirname, '../../src/infinite-continuum');
      const files = fs.readdirSync(continuumDir);
      
      const requiredFiles = [
        'types.ts',
        'knowledge-accretion.ts',
        'semantic-reformation.ts',
        'algorithmic-evolution.ts',
        'infinite-composition.ts',
        'fabric-expansion.ts',
        'continuum-memory.ts',
        'index.ts'
      ];
      
      for (const fileName of requiredFiles) {
        expect(files).toContain(fileName);
      }
      
      testResults.push({
        name: 'Verify Infinite Continuum module structure',
        status: 'pass',
        duration: getTestDuration(startTime),
        details: { files: requiredFiles }
      });
    } catch (error) {
      testResults.push({
        name: 'Verify Infinite Continuum module structure',
        status: 'fail',
        duration: getTestDuration(startTime),
        error: error instanceof Error ? error.message : String(error)
      });
      throw error;
    }
  });

  test('2.2 Verify Continuum exports all required systems', async () => {
    const startTime = Date.now();
    try {
      const indexPath = path.join(__dirname, '../../src/infinite-continuum/index.ts');
      const content = fs.readFileSync(indexPath, 'utf-8');
      
      const requiredExports = [
        'KnowledgeAccretionSystem',
        'SemanticReformationSystem',
        'AlgorithmicEvolutionSystem',
        'InfiniteCompositionEngine',
        'FabricExpansionSystem',
        'ContinuumMemorySystem'
      ];
      
      for (const exportName of requiredExports) {
        expect(content).toContain(exportName);
      }
      
      testResults.push({
        name: 'Verify Continuum exports all required systems',
        status: 'pass',
        duration: getTestDuration(startTime),
        details: { exports: requiredExports }
      });
    } catch (error) {
      testResults.push({
        name: 'Verify Continuum exports all required systems',
        status: 'fail',
        duration: getTestDuration(startTime),
        error: error instanceof Error ? error.message : String(error)
      });
      throw error;
    }
  });

  test('2.3 Verify Continuum integration in Fabric Continuum file', async () => {
    const startTime = Date.now();
    try {
      const integrationPath = path.join(__dirname, '../../code-intelligence-security-layer/fabric-continuum-integration.ts');
      const content = fs.readFileSync(integrationPath, 'utf-8');
      
      const continuumImports = [
        'KnowledgeAccretionSystem',
        'SemanticReformationSystem',
        'AlgorithmicEvolutionSystem',
        'InfiniteCompositionEngine',
        'FabricExpansionSystem',
        'ContinuumMemorySystem'
      ];
      
      for (const importName of continuumImports) {
        expect(content).toContain(importName);
      }
      
      testResults.push({
        name: 'Verify Continuum integration in Fabric Continuum file',
        status: 'pass',
        duration: getTestDuration(startTime),
        details: { imports: continuumImports }
      });
    } catch (error) {
      testResults.push({
        name: 'Verify Continuum integration in Fabric Continuum file',
        status: 'fail',
        duration: getTestDuration(startTime),
        error: error instanceof Error ? error.message : String(error)
      });
      throw error;
    }
  });
});

// ============================================================================
// Integration Test Suite 3: Pipeline ↔ Connector Integration
// ============================================================================

describe('Integration Test Suite 3: Pipeline ↔ Connector Integration', () => {
  let suite: IntegrationTestSuite;
  const testResults: TestResult[] = [];

  beforeEach(() => {
    suite = {
      name: 'Pipeline ↔ Connector Integration',
      tests: [],
      startTime: Date.now(),
      endTime: 0,
      status: 'pass'
    };
  });

  afterEach(() => {
    suite.endTime = Date.now();
    suite.tests = testResults;
    suite.status = testResults.every(r => r.status === 'pass') ? 'pass' : 
                   testResults.some(r => r.status === 'pass') ? 'partial' : 'fail';
    
    console.log(`\n=== Suite Complete: ${suite.name} ===`);
    console.log(`Duration: ${formatDuration(suite.endTime - suite.startTime)}`);
    console.log(`Status: ${suite.status}`);
    console.log(`Tests: ${testResults.length}`);
  });

  test('3.1 Verify Git Connector exists and exports', async () => {
    const startTime = Date.now();
    try {
      const connectorPath = path.join(__dirname, '../../src/connectors/git-connector.ts');
      const exists = fs.existsSync(connectorPath);
      
      expect(exists).toBe(true);
      
      const content = fs.readFileSync(connectorPath, 'utf-8');
      expect(content).toContain('export class GitConnector');
      
      testResults.push({
        name: 'Verify Git Connector exists and exports',
        status: 'pass',
        duration: getTestDuration(startTime),
        details: { path: connectorPath }
      });
    } catch (error) {
      testResults.push({
        name: 'Verify Git Connector exists and exports',
        status: 'fail',
        duration: getTestDuration(startTime),
        error: error instanceof Error ? error.message : String(error)
      });
      throw error;
    }
  });

  test('3.2 Verify Infinite Continuum Server exists', async () => {
    const startTime = Date.now();
    try {
      const serverPath = path.join(__dirname, '../../src/infinite-continuum-server.ts');
      const exists = fs.existsSync(serverPath);
      
      expect(exists).toBe(true);
      
      const content = fs.readFileSync(serverPath, 'utf-8');
      expect(content).toContain('express');
      expect(content).toContain('app');
      
      testResults.push({
        name: 'Verify Infinite Continuum Server exists',
        status: 'pass',
        duration: getTestDuration(startTime),
        details: { path: serverPath }
      });
    } catch (error) {
      testResults.push({
        name: 'Verify Infinite Continuum Server exists',
        status: 'fail',
        duration: getTestDuration(startTime),
        error: error instanceof Error ? error.message : String(error)
      });
      throw error;
    }
  });

  test('3.3 Verify Server imports Infinite Continuum', async () => {
    const startTime = Date.now();
    try {
      const serverPath = path.join(__dirname, '../../src/infinite-continuum-server.ts');
      const content = fs.readFileSync(serverPath, 'utf-8');
      
      const continuumImports = [
        'KnowledgeAccretion',
        'SemanticReformation',
        'AlgorithmicEvolution',
        'InfiniteComposition',
        'FabricExpansion',
        'ContinuumMemory'
      ];
      
      for (const importName of continuumImports) {
        expect(content).toContain(importName);
      }
      
      testResults.push({
        name: 'Verify Server imports Infinite Continuum',
        status: 'pass',
        duration: getTestDuration(startTime),
        details: { imports: continuumImports }
      });
    } catch (error) {
      testResults.push({
        name: 'Verify Server imports Infinite Continuum',
        status: 'fail',
        duration: getTestDuration(startTime),
        error: error instanceof Error ? error.message : String(error)
      });
      throw error;
    }
  });
});

// ============================================================================
// Integration Test Suite 4: End-to-End Workflows
// ============================================================================

describe('Integration Test Suite 4: End-to-End Workflows', () => {
  let suite: IntegrationTestSuite;
  const testResults: TestResult[] = [];

  beforeEach(() => {
    suite = {
      name: 'End-to-End Workflows',
      tests: [],
      startTime: Date.now(),
      endTime: 0,
      status: 'pass'
    };
  });

  afterEach(() => {
    suite.endTime = Date.now();
    suite.tests = testResults;
    suite.status = testResults.every(r => r.status === 'pass') ? 'pass' : 
                   testResults.some(r => r.status === 'pass') ? 'partial' : 'fail';
    
    console.log(`\n=== Suite Complete: ${suite.name} ===`);
    console.log(`Duration: ${formatDuration(suite.endTime - suite.startTime)}`);
    console.log(`Status: ${suite.status}`);
    console.log(`Tests: ${testResults.length}`);
  });

  test('4.1 Verify Capability Generation flow components', async () => {
    const startTime = Date.now();
    try {
      // Verify Generator Engine
      const generatorPath = path.join(__dirname, '../../code-intelligence-security-layer/generator-engine/index.ts');
      expect(fs.existsSync(generatorPath)).toBe(true);
      
      // Verify Capability Schema
      const schemaPath = path.join(__dirname, '../../code-intelligence-security-layer/capability-schema/index.ts');
      expect(fs.existsSync(schemaPath)).toBe(true);
      
      // Verify Pattern Library
      const patternPath = path.join(__dirname, '../../code-intelligence-security-layer/pattern-library/index.ts');
      expect(fs.existsSync(patternPath)).toBe(true);
      
      testResults.push({
        name: 'Verify Capability Generation flow components',
        status: 'pass',
        duration: getTestDuration(startTime),
        details: {
          generator: generatorPath,
          schema: schemaPath,
          pattern: patternPath
        }
      });
    } catch (error) {
      testResults.push({
        name: 'Verify Capability Generation flow components',
        status: 'fail',
        duration: getTestDuration(startTime),
        error: error instanceof Error ? error.message : String(error)
      });
      throw error;
    }
  });

  test('4.2 Verify Pattern Matching flow components', async () => {
    const startTime = Date.now();
    try {
      // Verify Pattern Library exists
      const patternDir = path.join(__dirname, '../../code-intelligence-security-layer/pattern-library');
      const dirs = fs.readdirSync(patternDir);
      
      const requiredPatternDirs = ['security-patterns', 'performance-patterns', 'architecture-patterns'];
      
      for (const dirName of requiredPatternDirs) {
        expect(dirs).toContain(dirName);
      }
      
      testResults.push({
        name: 'Verify Pattern Matching flow components',
        status: 'pass',
        duration: getTestDuration(startTime),
        details: { directories: requiredPatternDirs }
      });
    } catch (error) {
      testResults.push({
        name: 'Verify Pattern Matching flow components',
        status: 'fail',
        duration: getTestDuration(startTime),
        error: error instanceof Error ? error.message : String(error)
      });
      throw error;
    }
  });

  test('4.3 Verify Deployment Weaver flow components', async () => {
    const startTime = Date.now();
    try {
      // Verify Deployment Weaver
      const weaverPath = path.join(__dirname, '../../code-intelligence-security-layer/deployment-weaver/index.ts');
      expect(fs.existsSync(weaverPath)).toBe(true);
      
      // Verify deployment platforms
      const weaverDir = path.join(__dirname, '../../code-intelligence-security-layer/deployment-weaver');
      const dirs = fs.readdirSync(weaverDir);
      
      const requiredPlatforms = ['cli-generator', 'ide-extension', 'web-console', 'ci-cd-integration'];
      
      for (const platformName of requiredPlatforms) {
        expect(dirs).toContain(platformName);
      }
      
      testResults.push({
        name: 'Verify Deployment Weaver flow components',
        status: 'pass',
        duration: getTestDuration(startTime),
        details: { platforms: requiredPlatforms }
      });
    } catch (error) {
      testResults.push({
        name: 'Verify Deployment Weaver flow components',
        status: 'fail',
        duration: getTestDuration(startTime),
        error: error instanceof Error ? error.message : String(error)
      });
      throw error;
    }
  });
});