# @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: ultra-strict-verification-core-test
# @GL-charter-version: 2.0.0

/**
 * Ultra-Strict Verification Core - Test Runner
 * 
 * Purpose: Run verification tests against existing GL system
 */

import { UltraStrictVerificationCore } from './index';

async function runVerificationTests() {
  console.log('='.repeat(80));
  console.log('GL Ultra-Strict Verification Core - Test Runner');
  console.log('='.repeat(80));
  console.log('');

  const verificationCore = new UltraStrictVerificationCore();

  // Test components
  const testComponents = [
    'unified-intelligence-fabric',
    'infinite-continuum',
    'code-intel-security-layer'
  ];

  const results = [];

  for (const component of testComponents) {
    console.log(`\n${'='.repeat(80)}`);
    console.log(`Testing component: ${component}`);
    console.log('='.repeat(80));

    try {
      const result = await verificationCore.executeFullVerification({
        component,
        strictness: 'ultra',
        stopOnFirstFailure: false,
        requireEvidence: true,
        requireFalsification: true,
        requireBaseline: false,
        requireOracle: false,
        timeout: 60000
      });

      results.push({
        component,
        status: result.overallStatus,
        findings: result.summary.totalFindings,
        critical: result.summary.criticalFindings,
        high: result.summary.highFindings,
        medium: result.summary.mediumFindings
      });

      console.log(`\n✓ Verification completed`);
      console.log(`  Status: ${result.overallStatus}`);
      console.log(`  Total findings: ${result.summary.totalFindings}`);
      console.log(`  Critical: ${result.summary.criticalFindings}`);
      console.log(`  High: ${result.summary.highFindings}`);
      console.log(`  Medium: ${result.summary.mediumFindings}`);
      console.log(`  Low: ${result.summary.lowFindings}`);
      console.log(`  Info: ${result.summary.infoFindings}`);

      // Print top findings
      if (result.findings.length > 0) {
        console.log(`\n  Top findings:`);
        for (let i = 0; i