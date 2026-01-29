// @GL-governed
// @GL-layer: GL90-99
// @GL-semantic: run-integration-tests-simple
// @GL-charter-version: 4.0.0
// @GL-audit-trail: ../../engine/governance/GL_SEMANTIC_ANCHOR.json

/**
 * GL Runtime Platform - Simple Integration Test Runner
 * Version 21.0.0
 * 
 * 執行整合測試套件並生成報告（不依賴 Jest）
 */

import * as path from 'path';
import * as fs from 'fs';

// ============================================================================
// Configuration
// ============================================================================

const TEST_OUTPUT_DIR = path.join(__dirname, '../test-reports');

// ============================================================================
// Test Results
// ============================================================================

interface TestResult {
  name: string;
  status: 'pass' | 'fail' | 'skip';
  duration: number;
  error?: string;
  details?: any;
}

interface TestSuite {
  name: string;
  tests: TestResult[];
  startTime: number;
  endTime: number;
  status: 'pass' | 'fail' | 'partial';
}

interface IntegrationTestReport {
  timestamp: string;
  version: string;
  totalSuites: number;
  totalTests: number;
  totalPassed: number;
  totalFailed: number;
  totalSkipped: number;
  totalDuration: number;
  passRate: number;
  suites: TestSuite[];
  summary: string;
  status: 'pass' | 'fail' | 'partial';
}

// ============================================================================
// Utility Functions
// ============================================================================

function ensureOutputDir(): void {
  if (!fs.existsSync(TEST_OUTPUT_DIR)) {
    fs.mkdirSync(TEST_OUTPUT_DIR, { recursive: true });
  }
}

function formatDuration(ms: number): string {
  if (ms < 1000) return `${ms}ms`;
  return `${(ms / 1000).toFixed(2)}s`;
}

function getTimestamp(): string {
  return new Date().toISOString();
}

function getTestDuration(startTime: number): number {
  return Date.now() - startTime;
}

// ============================================================================
// Test Functions
// ============================================================================

async function runTest(testName: string, testFn: () => Promise<void> | void): Promise<TestResult> {
  const startTime = Date.now();
  try {
    await testFn();
    return {
      name: testName,
      status: 'pass',
      duration: getTestDuration(startTime)
    };
  } catch (error) {
    return {
      name: testName,
      status: 'fail',
      duration: getTestDuration(startTime),
      error: error instanceof Error ? error.message : String(error)
    };
  }
}

// ============================================================================
// Test Suite 1: V19 Fabric ↔ Code Intelligence Layer
// ============================================================================

async function runTestSuite1(): Promise<TestSuite> {
  const suite: TestSuite = {
    name: 'V19 Fabric ↔ Code Intelligence Layer',
    tests: [],
    startTime: Date.now(),
    endTime: 0,
    status: 'pass'
  };
  
  console.log(`\n=== Running: ${suite.name} ===`);
  
  // Test 1.1
  suite.tests.push(await runTest(
    '1.1 Verify Fabric Continuum Integration file exists',
    async () => {
      const integrationPath = path.join(__dirname, '../code-intel-security-layer/fabric-continuum-integration.ts');
      if (!fs.existsSync(integrationPath)) {
        throw new Error(`File not found: ${integrationPath}`);
      }
    }
  ));
  
  // Test 1.2
  suite.tests.push(await runTest(
    '1.2 Verify integration exports required classes',
    async () => {
      const integrationPath = path.join(__dirname, '../code-intel-security-layer/index.ts');
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
        if (!content.includes(`export ${exportName}`)) {
          throw new Error(`Missing export: ${exportName}`);
        }
      }
    }
  ));
  
  // Test 1.3
  suite.tests.push(await runTest(
    '1.3 Verify Fabric Continuum Integration types',
    async () => {
      const integrationPath = path.join(__dirname, '../code-intel-security-layer/fabric-continuum-integration.ts');
      const content = fs.readFileSync(integrationPath, 'utf-8');
      
      const requiredTypes = [
        'FabricContinuumIntegrationConfig',
        'IntegratedCapabilityRequest',
        'IntegratedCapabilityResponse',
        'FabricContinuumMetrics'
      ];
      
      for (const typeName of requiredTypes) {
        if (!content.includes(`export interface ${typeName}`)) {
          throw new Error(`Missing type: ${typeName}`);
        }
      }
    }
  ));
  
  suite.endTime = Date.now();
  suite.status = suite.tests.every(t => t.status === 'pass') ? 'pass' : 
                 suite.tests.some(t => t.status === 'pass') ? 'partial' : 'fail';
  
  printSuiteResults(suite);
  return suite;
}

// ============================================================================
// Test Suite 2: V20 Continuum ↔ Code Intelligence Layer
// ============================================================================

async function runTestSuite2(): Promise<TestSuite> {
  const suite: TestSuite = {
    name: 'V20 Continuum ↔ Code Intelligence Layer',
    tests: [],
    startTime: Date.now(),
    endTime: 0,
    status: 'pass'
  };
  
  console.log(`\n=== Running: ${suite.name} ===`);
  
  // Test 2.1
  suite.tests.push(await runTest(
    '2.1 Verify Infinite Continuum module structure',
    async () => {
      const continuumDir = path.join(__dirname, '../src/infinite-continuum');
      if (!fs.existsSync(continuumDir)) {
        throw new Error(`Directory not found: ${continuumDir}`);
      }
      
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
        if (!files.includes(fileName)) {
          throw new Error(`Missing file: ${fileName}`);
        }
      }
    }
  ));
  
  // Test 2.2
  suite.tests.push(await runTest(
    '2.2 Verify Continuum exports all required systems',
    async () => {
      const indexPath = path.join(__dirname, '../src/infinite-continuum/index.ts');
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
        if (!content.includes(exportName)) {
          throw new Error(`Missing export: ${exportName}`);
        }
      }
    }
  ));
  
  // Test 2.3
  suite.tests.push(await runTest(
    '2.3 Verify Continuum integration in Fabric Continuum file',
    async () => {
      const integrationPath = path.join(__dirname, '../code-intel-security-layer/fabric-continuum-integration.ts');
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
        if (!content.includes(importName)) {
          throw new Error(`Missing import: ${importName}`);
        }
      }
    }
  ));
  
  suite.endTime = Date.now();
  suite.status = suite.tests.every(t => t.status === 'pass') ? 'pass' : 
                 suite.tests.some(t => t.status === 'pass') ? 'partial' : 'fail';
  
  printSuiteResults(suite);
  return suite;
}

// ============================================================================
// Test Suite 3: Pipeline ↔ Connector Integration
// ============================================================================

async function runTestSuite3(): Promise<TestSuite> {
  const suite: TestSuite = {
    name: 'Pipeline ↔ Connector Integration',
    tests: [],
    startTime: Date.now(),
    endTime: 0,
    status: 'pass'
  };
  
  console.log(`\n=== Running: ${suite.name} ===`);
  
  // Test 3.1
  suite.tests.push(await runTest(
    '3.1 Verify Git Connector exists and exports',
    async () => {
      const connectorPath = path.join(__dirname, '../src/connectors/git-connector.ts');
      if (!fs.existsSync(connectorPath)) {
        throw new Error(`File not found: ${connectorPath}`);
      }
      
      const content = fs.readFileSync(connectorPath, 'utf-8');
      if (!content.includes('export class GitConnector')) {
        throw new Error('Missing GitConnector export');
      }
    }
  ));
  
  // Test 3.2
  suite.tests.push(await runTest(
    '3.2 Verify Infinite Continuum Server exists',
    async () => {
      const serverPath = path.join(__dirname, '../src/infinite-continuum-server.ts');
      if (!fs.existsSync(serverPath)) {
        throw new Error(`File not found: ${serverPath}`);
      }
      
      const content = fs.readFileSync(serverPath, 'utf-8');
      if (!content.includes('express') || !content.includes('app')) {
        throw new Error('Server missing express or app');
      }
    }
  ));
  
  // Test 3.3
  suite.tests.push(await runTest(
    '3.3 Verify Server imports Infinite Continuum',
    async () => {
      const serverPath = path.join(__dirname, '../src/infinite-continuum-server.ts');
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
        if (!content.includes(importName)) {
          throw new Error(`Missing import: ${importName}`);
        }
      }
    }
  ));
  
  suite.endTime = Date.now();
  suite.status = suite.tests.every(t => t.status === 'pass') ? 'pass' : 
                 suite.tests.some(t => t.status === 'pass') ? 'partial' : 'fail';
  
  printSuiteResults(suite);
  return suite;
}

// ============================================================================
// Test Suite 4: End-to-End Workflows
// ============================================================================

async function runTestSuite4(): Promise<TestSuite> {
  const suite: TestSuite = {
    name: 'End-to-End Workflows',
    tests: [],
    startTime: Date.now(),
    endTime: 0,
    status: 'pass'
  };
  
  console.log(`\n=== Running: ${suite.name} ===`);
  
  // Test 4.1
  suite.tests.push(await runTest(
    '4.1 Verify Capability Generation flow components',
    async () => {
      const generatorPath = path.join(__dirname, '../code-intel-security-layer/generator-engine/index.ts');
      const schemaPath = path.join(__dirname, '../code-intel-security-layer/capability-schema/index.ts');
      const patternPath = path.join(__dirname, '../code-intel-security-layer/pattern-library/index.ts');
      
      if (!fs.existsSync(generatorPath)) {
        throw new Error(`File not found: ${generatorPath}`);
      }
      if (!fs.existsSync(schemaPath)) {
        throw new Error(`File not found: ${schemaPath}`);
      }
      if (!fs.existsSync(patternPath)) {
        throw new Error(`File not found: ${patternPath}`);
      }
    }
  ));
  
  // Test 4.2
  suite.tests.push(await runTest(
    '4.2 Verify Pattern Matching flow components',
    async () => {
      const patternDir = path.join(__dirname, '../code-intel-security-layer/pattern-library');
      const dirs = fs.readdirSync(patternDir);
      
      const requiredPatternDirs = ['security-patterns', 'performance-patterns', 'architecture-patterns'];
      
      for (const dirName of requiredPatternDirs) {
        if (!dirs.includes(dirName)) {
          throw new Error(`Missing directory: ${dirName}`);
        }
      }
    }
  ));
  
  // Test 4.3
  suite.tests.push(await runTest(
    '4.3 Verify Deployment Weaver flow components',
    async () => {
      const weaverPath = path.join(__dirname, '../code-intel-security-layer/deployment-weaver/index.ts');
      if (!fs.existsSync(weaverPath)) {
        throw new Error(`File not found: ${weaverPath}`);
      }
      
      const weaverDir = path.join(__dirname, '../code-intel-security-layer/deployment-weaver');
      const dirs = fs.readdirSync(weaverDir);
      
      const requiredPlatforms = ['cli-generator', 'ide-extension', 'web-console', 'ci-cd-integration'];
      
      for (const platformName of requiredPlatforms) {
        if (!dirs.includes(platformName)) {
          throw new Error(`Missing platform: ${platformName}`);
        }
      }
    }
  ));
  
  suite.endTime = Date.now();
  suite.status = suite.tests.every(t => t.status === 'pass') ? 'pass' : 
                 suite.tests.some(t => t.status === 'pass') ? 'partial' : 'fail';
  
  printSuiteResults(suite);
  return suite;
}

// ============================================================================
// Print Suite Results
// ============================================================================

function printSuiteResults(suite: TestSuite): void {
  console.log(`\nDuration: ${formatDuration(suite.endTime - suite.startTime)}`);
  console.log(`Status: ${suite.status === 'pass' ? '✅ PASS' : suite.status === 'partial' ? '⚠️ PARTIAL' : '❌ FAIL'}`);
  console.log(`Tests: ${suite.tests.length}`);
  console.log(`  Passed: ${suite.tests.filter(t => t.status === 'pass').length}`);
  console.log(`  Failed: ${suite.tests.filter(t => t.status === 'fail').length}`);
  
  for (const test of suite.tests) {
    const icon = test.status === 'pass' ? '✅' : '❌';
    console.log(`  ${icon} ${test.name} (${formatDuration(test.duration)})`);
    if (test.error) {
      console.log(`     Error: ${test.error}`);
    }
  }
}

// ============================================================================
// Run All Tests
// ============================================================================

async function runAllTests(): Promise<IntegrationTestReport> {
  console.log('\n========================================');
  console.log('GL Runtime Platform Integration Tests');
  console.log('========================================');
  console.log(`Version: 21.0.0`);
  console.log(`Timestamp: ${getTimestamp()}\n`);
  
  const report: IntegrationTestReport = {
    timestamp: getTimestamp(),
    version: '21.0.0',
    totalSuites: 0,
    totalTests: 0,
    totalPassed: 0,
    totalFailed: 0,
    totalSkipped: 0,
    totalDuration: 0,
    passRate: 0,
    suites: [],
    summary: '',
    status: 'pass'
  };
  
  const startTime = Date.now();
  
  // Run all test suites
  report.suites.push(await runTestSuite1());
  report.suites.push(await runTestSuite2());
  report.suites.push(await runTestSuite3());
  report.suites.push(await runTestSuite4());
  
  report.totalDuration = Date.now() - startTime;
  report.totalSuites = report.suites.length;
  
  // Calculate totals
  for (const suite of report.suites) {
    report.totalTests += suite.tests.length;
    report.totalPassed += suite.tests.filter(t => t.status === 'pass').length;
    report.totalFailed += suite.tests.filter(t => t.status === 'fail').length;
    report.totalSkipped += suite.tests.filter(t => t.status === 'skip').length;
  }
  
  // Calculate pass rate
  if (report.totalTests > 0) {
    report.passRate = (report.totalPassed / report.totalTests) * 100;
  }
  
  // Determine overall status
  report.status = report.totalFailed === 0 ? 'pass' : 
                  report.totalPassed > 0 ? 'partial' : 'fail';
  
  report.summary = `Integration Tests: ${report.totalPassed}/${report.totalTests} passed (${report.passRate.toFixed(1)}%) in ${formatDuration(report.totalDuration)}`;
  
  return report;
}

// ============================================================================
// Save Test Report
// ============================================================================

function saveTestReport(report: IntegrationTestReport): void {
  ensureOutputDir();
  
  // Save JSON report
  const jsonPath = path.join(TEST_OUTPUT_DIR, 'integration-test-report.json');
  fs.writeFileSync(jsonPath, JSON.stringify(report, null, 2));
  console.log(`\n✅ JSON report saved: ${jsonPath}`);
  
  // Save markdown report
  const mdPath = path.join(TEST_OUTPUT_DIR, 'integration-test-report.md');
  const markdown = generateMarkdownReport(report);
  fs.writeFileSync(mdPath, markdown);
  console.log(`✅ Markdown report saved: ${mdPath}`);
}

// ============================================================================
// Generate Markdown Report
// ============================================================================

function generateMarkdownReport(report: IntegrationTestReport): string {
  let md = `# @GL-governed\n# @GL-layer: GL90-99\n# @GL-semantic: integration-test-report\n# @GL-charter-version: 4.0.0\n# @GL-audit-trail: ../../engine/governance/GL_SEMANTIC_ANCHOR.json\n\n`;
  md += `# Integration Test Report\n\n`;
  md += `**Generated:** ${report.timestamp}\n`;
  md += `**Version:** ${report.version}\n\n`;
  
  md += `## Summary\n\n`;
  md += `| Metric | Value |\n`;
  md += `|--------|-------|\n`;
  md += `| Total Suites | ${report.totalSuites} |\n`;
  md += `| Total Tests | ${report.totalTests} |\n`;
  md += `| Passed | ${report.totalPassed} |\n`;
  md += `| Failed | ${report.totalFailed} |\n`;
  md += `| Skipped | ${report.totalSkipped} |\n`;
  md += `| Pass Rate | ${report.passRate.toFixed(1)}% |\n`;
  md += `| Duration | ${formatDuration(report.totalDuration)} |\n`;
  md += `| Status | ${report.status === 'pass' ? '✅ PASS' : report.status === 'partial' ? '⚠️ PARTIAL' : '❌ FAIL'} |\n\n`;
  
  md += `**${report.summary}**\n\n`;
  
  md += `## Test Suites\n\n`;
  
  for (const suite of report.suites) {
    md += `### ${suite.name}\n\n`;
    md += `| Metric | Value |\n`;
    md += `|--------|-------|\n`;
    md += `| Tests | ${suite.tests.length} |\n`;
    md += `| Passed | ${suite.tests.filter(t => t.status === 'pass').length} |\n`;
    md += `| Failed | ${suite.tests.filter(t => t.status === 'fail').length} |\n`;
    md += `| Duration | ${formatDuration(suite.endTime - suite.startTime)} |\n`;
    md += `| Status | ${suite.status === 'pass' ? '✅' : suite.status === 'partial' ? '⚠️' : '❌'} |\n\n`;
    
    md += `#### Test Details\n\n`;
    for (const test of suite.tests) {
      const icon = test.status === 'pass' ? '✅' : test.status === 'skip' ? '⏭️' : '❌';
      md += `- ${icon} **${test.name}** (${formatDuration(test.duration)})\n`;
      if (test.error) {
        md += `  - Error: ${test.error}\n`;
      }
    }
    md += `\n`;
  }
  
  return md;
}

// ============================================================================
// Print Report Summary
// ============================================================================

function printReportSummary(report: IntegrationTestReport): void {
  console.log('\n========================================');
  console.log('Integration Test Results Summary');
  console.log('========================================\n');
  
  console.log(`Total Suites: ${report.totalSuites}`);
  console.log(`Total Tests: ${report.totalTests}`);
  console.log(`Passed: ${report.totalPassed}`);
  console.log(`Failed: ${report.totalFailed}`);
  console.log(`Skipped: ${report.totalSkipped}`);
  console.log(`Pass Rate: ${report.passRate.toFixed(1)}%`);
  console.log(`Duration: ${formatDuration(report.totalDuration)}`);
  console.log(`Status: ${report.status === 'pass' ? '✅ PASS' : report.status === 'partial' ? '⚠️ PARTIAL' : '❌ FAIL'}`);
  console.log(`\n${report.summary}\n`);
}

// ============================================================================
// Main Execution
// ============================================================================

async function main(): Promise<void> {
  const report = await runAllTests();
  saveTestReport(report);
  printReportSummary(report);
  
  // Exit with appropriate code
  process.exit(report.status === 'pass' ? 0 : 1);
}

// Run if executed directly
if (require.main === module) {
  main().catch(error => {
    console.error('Fatal error:', error);
    process.exit(1);
  });
}

export { runAllTests, saveTestReport, printReportSummary };