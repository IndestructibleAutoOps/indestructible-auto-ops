// @GL-governed
// @GL-layer: GL90-99
// @GL-semantic: run-integration-tests
// @GL-charter-version: 4.0.0
// @GL-audit-trail: ../../engine/governance/GL_SEMANTIC_ANCHOR.json

/**
 * GL Runtime Platform - Integration Test Runner
 * Version 21.0.0
 * 
 * 執行整合測試套件並生成報告
 */

import { execSync } from 'child_process';
import * as path from 'path';
import * as fs from 'fs';

// ============================================================================
// Configuration
// ============================================================================

const TEST_OUTPUT_DIR = path.join(__dirname, '../test-reports');
const INTEGRATION_TEST_FILE = path.join(__dirname, 'integration/integration-test-suite.ts');

// ============================================================================
// Test Results
// ============================================================================

interface TestSuiteResult {
  name: string;
  tests: number;
  passed: number;
  failed: number;
  skipped: number;
  duration: number;
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
  suites: TestSuiteResult[];
  summary: string;
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

// ============================================================================
// Parse Jest Output
// ============================================================================

function parseJestOutput(output: string): IntegrationTestReport {
  const lines = output.split('\n');
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
    summary: ''
  };
  
  // Parse test results from Jest output
  const passMatch = output.match(/Tests:\s+(\d+)\s+passed,\s+(\d+)\s+failed/);
  if (passMatch) {
    report.totalTests = parseInt(passMatch[1]) + parseInt(passMatch[2]);
    report.totalPassed = parseInt(passMatch[1]);
    report.totalFailed = parseInt(passMatch[2]);
    report.passRate = (report.totalPassed / report.totalTests) * 100;
  }
  
  // Parse duration
  const durationMatch = output.match(/Time:\s+([0-9.]+)\s*s/);
  if (durationMatch) {
    report.totalDuration = parseFloat(durationMatch[1]) * 1000;
  }
  
  // Determine status
  report.status = report.totalFailed === 0 ? 'pass' : 
                  report.totalPassed > 0 ? 'partial' : 'fail';
  
  // Generate summary
  report.summary = `Integration Tests: ${report.totalPassed}/${report.totalTests} passed (${report.passRate.toFixed(1)}%) in ${formatDuration(report.totalDuration)}`;
  
  return report;
}

// ============================================================================
// Run Integration Tests
// ============================================================================

function runIntegrationTests(): IntegrationTestReport {
  console.log('\n========================================');
  console.log('Running GL Runtime Platform Integration Tests');
  console.log('========================================\n');
  
  console.log(`Test File: ${INTEGRATION_TEST_FILE}`);
  console.log(`Output Directory: ${TEST_OUTPUT_DIR}\n`);
  
  try {
    // Run Jest tests
    const jestCommand = `npx jest ${INTEGRATION_TEST_FILE} --verbose --json --outputFile=${path.join(TEST_OUTPUT_DIR, 'jest-integration-results.json')}`;
    console.log(`Executing: ${jestCommand}\n`);
    
    const output = execSync(jestCommand, {
      encoding: 'utf-8',
      stdio: 'inherit',
      cwd: path.join(__dirname, '..')
    });
    
    console.log('\nTests completed successfully!\n');
    
    // Parse results from Jest JSON output
    const jestResultsPath = path.join(TEST_OUTPUT_DIR, 'jest-integration-results.json');
    let report: IntegrationTestReport;
    
    if (fs.existsSync(jestResultsPath)) {
      const jestData = JSON.parse(fs.readFileSync(jestResultsPath, 'utf-8'));
      report = parseJestResultsFromJson(jestData);
    } else {
      report = parseJestOutput(output);
    }
    
    return report;
    
  } catch (error) {
    console.error('\n❌ Tests failed!\n');
    console.error(error);
    
    // Try to parse partial results from Jest output
    try {
      const jestResultsPath = path.join(TEST_OUTPUT_DIR, 'jest-integration-results.json');
      if (fs.existsSync(jestResultsPath)) {
        const jestData = JSON.parse(fs.readFileSync(jestResultsPath, 'utf-8'));
        return parseJestResultsFromJson(jestData);
      }
    } catch (e) {
      // Ignore parsing errors
    }
    
    // Return failed report
    return {
      timestamp: getTimestamp(),
      version: '21.0.0',
      totalSuites: 0,
      totalTests: 0,
      totalPassed: 0,
      totalFailed: 1,
      totalSkipped: 0,
      totalDuration: 0,
      passRate: 0,
      suites: [],
      summary: 'Tests failed to execute',
      status: 'fail'
    };
  }
}

// ============================================================================
// Parse Jest Results from JSON
// ============================================================================

function parseJestResultsFromJson(jestData: any): IntegrationTestReport {
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
    summary: ''
  };
  
  if (jestData.testResults) {
    report.totalSuites = jestData.testResults.length;
    
    for (const suiteResult of jestData.testResults) {
      const suite: TestSuiteResult = {
        name: suiteResult.name,
        tests: suiteResult.numFailingTests + suiteResult.numPassingTests + suiteResult.numPendingTests,
        passed: suiteResult.numPassingTests,
        failed: suiteResult.numFailingTests,
        skipped: suiteResult.numPendingTests,
        duration: suiteResult.perfStats.end - suiteResult.perfStats.start,
        status: suiteResult.numFailingTests === 0 ? 'pass' : 'partial'
      };
      
      report.totalTests += suite.tests;
      report.totalPassed += suite.passed;
      report.totalFailed += suite.failed;
      report.totalSkipped += suite.skipped;
      report.totalDuration += suite.duration;
      report.suites.push(suite);
    }
  }
  
  if (report.totalTests > 0) {
    report.passRate = (report.totalPassed / report.totalTests) * 100;
  }
  
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
  let md = `# Integration Test Report\n\n`;
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
  
  if (report.suites.length > 0) {
    md += `## Test Suites\n\n`;
    
    for (const suite of report.suites) {
      md += `### ${suite.name}\n\n`;
      md += `| Metric | Value |\n`;
      md += `|--------|-------|\n`;
      md += `| Tests | ${suite.tests} |\n`;
      md += `| Passed | ${suite.passed} |\n`;
      md += `| Failed | ${suite.failed} |\n`;
      md += `| Skipped | ${suite.skipped} |\n`;
      md += `| Duration | ${formatDuration(suite.duration)} |\n`;
      md += `| Status | ${suite.status === 'pass' ? '✅' : suite.status === 'partial' ? '⚠️' : '❌'} |\n\n`;
    }
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

function main(): void {
  const report = runIntegrationTests();
  saveTestReport(report);
  printReportSummary(report);
  
  // Exit with appropriate code
  process.exit(report.status === 'pass' ? 0 : 1);
}

// Run if executed directly
if (require.main === module) {
  main();
}

export { runIntegrationTests, saveTestReport, printReportSummary };