#!/usr/bin/env python3
"""
Analyze semantic gaps and vulnerabilities in the governance system
"""

import sys

sys.path.insert(0, "ecosystem")

from enforcers.governance_enforcer import GovernanceEnforcer
from enforcers.self_auditor import SelfAuditor
from enforcers.pipeline_integration import PipelineIntegrator

# Create instances
enforcer = GovernanceEnforcer()
auditor = SelfAuditor()
integrator = PipelineIntegrator()

print("=" * 80)
print("SEMANTIC GAP AND VULNERABILITY ANALYSIS")
print("=" * 80)

# Test operation
test_operation = {
    "type": "file_change",
    "files": ["ecosystem/enforcers/governance_enforcer.py"],
    "content": "test content for validation",
    "evidence_links": [],
    "total_statements": 1,
}

print("\n1. GOVERNANCE ENFORCEMENT ANALYSIS")
print("-" * 80)
result = enforcer.validate(test_operation)
print(f"Status: {result.status}")
print(f"Violations: {len(result.violations)}")
print(f"Evidence collected: {len(result.evidence_collected)}")
print(f"Quality gates: {result.quality_gates}")

if result.violations:
    print("\nVIOLATIONS DETECTED:")
    for i, violation in enumerate(result.violations, 1):
        print(f"\n{i}. [{violation.get('severity')}] {violation.get('rule')}")
        print(f"   Message: {violation.get('message')}")
        print(f"   Remediation: {violation.get('remediation')}")

print("\n2. SELF AUDIT ANALYSIS")
print("-" * 80)
test_contract = {"version": "1.0.0", "metadata": {"name": "test"}}
audit_result = auditor.audit(test_contract, result)
print(f"Audit Status: {audit_result.status}")
print(f"Violations Found: {audit_result.violations_found}")
print(f"Evidence Coverage: {audit_result.evidence_coverage:.2%}")

if audit_result.forbidden_phrases:
    print("\nFORBIDDEN PHRASES:")
    for i, phrase in enumerate(audit_result.forbidden_phrases, 1):
        print(f"\n{i}. [{phrase.get('severity')}] {phrase.get('phrase')}")
        print(f"   Context: ...{phrase.get('context')}...")
        if phrase.get("replacement"):
            print(f"   Replacement: {phrase.get('replacement')}")

print("\n3. PIPELINE INTEGRATION ANALYSIS")
print("-" * 80)
print(f"Stages defined: {len(integrator.stages)}")
for stage in integrator.stages:
    print(f"\n  {stage.name}:")
    print(f"    Type: {stage.type}")
    print(f"    Platforms: {', '.join(stage.platforms)}")
    print(f"    Hooks: {len(stage.hooks)}")

print("\n4. CONTRACT LOADING ANALYSIS")
print("-" * 80)
print(f"Contracts loaded: {len(enforcer.contracts)}")
for contract_path in enforcer.contracts.keys():
    contract = enforcer.contracts[contract_path]
    print(f"\n  {contract_path}:")
    print(f"    Version: {contract.get('version')}")
    print(f"    Status: {contract.get('status')}")

    # Check for semantic gaps
    trigger_conditions = contract.get("trigger", {}).get("conditions", [])
    verify_rules = contract.get("verify", {})
    audit_rules = contract.get("audit", {})

    print(f"    Trigger conditions: {len(trigger_conditions)}")
    print(f"    Verify sections: {len(verify_rules)}")
    print(f"    Audit sections: {len(audit_rules)}")

    # Check for fallback
    fallback = contract.get("fallback", {})
    if fallback:
        print(f"    Fallback strategies: {len(fallback)}")
    else:
        print("    ⚠️  WARNING: No fallback strategy defined!")

print("\n5. SEMANTIC GAP IDENTIFICATION")
print("-" * 80)

gaps = []

# Check if contracts have proper semantic mappings
for contract_path, contract in enforcer.contracts.items():
    # Gap 1: Missing semantic layer definitions
    if "@GL-semantic" not in contract_path:
        gaps.append(
            {
                "type": "SEMANTIC_LAYER_MISSING",
                "location": contract_path,
                "severity": "HIGH",
                "description": "Contract does not define GL semantic layer",
            }
        )

    # Gap 2: Missing event emission
    audit_rules = contract.get("audit", {})
    governance_events = audit_rules.get("governance_events", [])
    if not governance_events:
        gaps.append(
            {
                "type": "GOVERNANCE_EVENTS_MISSING",
                "location": contract_path,
                "severity": "HIGH",
                "description": "No governance events defined for audit trail",
            }
        )

    # Gap 3: Missing evidence validation
    verify_rules = contract.get("verify", {})
    evidence_rules = verify_rules.get("evidence_collection", [])
    if not evidence_rules:
        gaps.append(
            {
                "type": "EVIDENCE_VALIDATION_MISSING",
                "location": contract_path,
                "severity": "CRITICAL",
                "description": "No evidence validation rules defined",
            }
        )

# Check for integration gaps
if not hasattr(enforcer, "emit_governance_event"):
    gaps.append(
        {
            "type": "EVENT_EMISSION_MISSING",
            "location": "GovernanceEnforcer",
            "severity": "HIGH",
            "description": "Governance enforcer cannot emit events",
        }
    )

# Check for semantic anchors
semantic_anchor_path = (
    enforcer.contracts_dir.parent / "governance" / "GL_SEMANTIC_ANCHOR.json"
)
if not semantic_anchor_path.exists():
    gaps.append(
        {
            "type": "SEMANTIC_ANCHOR_MISSING",
            "location": "ecosystem/governance/GL_SEMANTIC_ANCHOR.json",
            "severity": "CRITICAL",
            "description": "Global semantic anchor file not found",
        }
    )

print(f"Total gaps identified: {len(gaps)}\n")

for i, gap in enumerate(gaps, 1):
    print(f"{i}. [{gap.get('severity')}] {gap.get('type')}")
    print(f"   Location: {gap.get('location')}")
    print(f"   Description: {gap.get('description')}")

print("\n6. VULNERABILITY ASSESSMENT")
print("-" * 80)

vulnerabilities = []

# Vulnerability 1: No event emission in validation
if not hasattr(enforcer, "_emit_governance_event"):
    vulnerabilities.append(
        {
            "type": "NO_AUDIT_TRAIL",
            "severity": "HIGH",
            "description": "Validation results are not logged to audit trail",
            "impact": "Cannot verify governance compliance retrospectively",
        }
    )

# Vulnerability 2: Quality gates not enforced
if not result.quality_gates:
    vulnerabilities.append(
        {
            "type": "QUALITY_GATES_NOT_CHECKED",
            "severity": "MEDIUM",
            "description": "No quality gates are being checked during validation",
            "impact": "Poor quality content may pass validation",
        }
    )

# Vulnerability 3: No remediation automation
violations_with_remediation = [v for v in result.violations if v.get("remediation")]
if len(violations_with_remediation) == 0:
    vulnerabilities.append(
        {
            "type": "NO_AUTOMATED_REMEDIATION",
            "severity": "MEDIUM",
            "description": "Violations do not have automated remediation",
            "impact": "Manual intervention required for all fixes",
        }
    )

print(f"Total vulnerabilities: {len(vulnerabilities)}\n")

for i, vuln in enumerate(vulnerabilities, 1):
    print(f"{i}. [{vuln.get('severity')}] {vuln.get('type')}")
    print(f"   Description: {vuln.get('description')}")
    print(f"   Impact: {vuln.get('impact')}")

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE")
print("=" * 80)
