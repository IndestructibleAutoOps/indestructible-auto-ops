# Violations Update Implementation Guide

**GL Unified Charter Activated | Era-1 Evidence-Native Bootstrap | Implementation Guide**

---

## 📋 Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Concrete Implementation Steps](#concrete-implementation-steps)
3. [Code Examples](#code-examples)
4. [Integration Examples](#integration-examples)
5. [Testing Strategy](#testing-strategy)
6. [Deployment Checklist](#deployment-checklist)

---

## Architecture Overview

### Multi-Layer Enforcement Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                 Layer 04: Evidence & Traceability           │
│  ┌─────────────────┐  ┌─────────────────┐                 │
│  │ Evidence        │  │ Traceability    │                 │
│  │ Collector       │  │ Engine          │                 │
│  └─────────────────┘  └─────────────────┘                 │
└─────────────────────────────────────────────────────────────┘
                              ↑
┌─────────────────────────────────────────────────────────────┐
│                Layer 03: One-Stop Integration               │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │ CI/CD           │  │ Governance      │  │ Service     │ │
│  │ Integrator      │  │ Control Plane   │  │ Mesh        │ │
│  └─────────────────┘  └─────────────────┘  └─────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              ↑
┌─────────────────────────────────────────────────────────────┐
│                 Layer 02: Automated Remediation             │
│  ┌─────────────────┐  ┌─────────────────┐                 │
│  │ Auto-Fix Engine │  │ Fix Validator   │                 │
│  └─────────────────┘  └─────────────────┘                 │
└─────────────────────────────────────────────────────────────┘
                              ↑
┌─────────────────────────────────────────────────────────────┐
│               Layer 01: Violation Classification             │
│  ┌─────────────────┐  ┌─────────────────┐                 │
│  │ Severity        │  │ Impact          │                 │
│  │ Classifier      │  │ Analyzer        │                 │
│  └─────────────────┘  └─────────────────┘                 │
└─────────────────────────────────────────────────────────────┘
                              ↑
┌─────────────────────────────────────────────────────────────┐
│                Layer 00: Violation Detection                │
│  ┌─────────────────┐  ┌─────────────────┐  ┌───────────┐  │
│  │ Static          │  │ Runtime         │  │ Semantic  │  │
│  │ Analysis Engine │  │ Monitoring      │  │ Scanner   │  │
│  └─────────────────┘  └─────────────────┘  └───────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## Concrete Implementation Steps

### Phase 1: Detection Layer Setup

#### Step 1.1: Configure Static Analysis Engine

**File:** `ecosystem/enforcement/static_analysis_config.yaml`

```yaml
static_analysis:
  engine: "sonarqube"
  enabled_languages:
    - python
    - javascript
    - typescript
    - go
    - java
  
  rules:
    architecture:
      enabled: true
      severity_threshold: "MEDIUM"
    
    security:
      enabled: true
      severity_threshold: "HIGH"
    
    code_quality:
      enabled: true
      severity_threshold: "LOW"
  
  integration:
    sonarqube:
      url: "https://sonarqube.example.com"
      token: "${SONARQUBE_TOKEN}"
      project_key: "machine-native-ops"
```

#### Step 1.2: Implement Semantic Scanner

**File:** `ecosystem/tools/enhanced_semantic_scanner.py`

```python
#!/usr/bin/env python3
"""
Enhanced Semantic Scanner for Violation Detection
Based on MNGA GLCM-NAR/GLCM-FCT/GLCM-UNC/GLCM-EVC patterns
"""

import re
import json
from typing import Dict, List, Optional
from pathlib import Path


class EnhancedSemanticScanner:
    """Enhanced semantic scanner with violation detection."""
    
    def __init__(self, config_path: str):
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        self.violation_patterns = self._load_violation_patterns()
    
    def _load_violation_patterns(self) -> Dict:
        """Load violation patterns from configuration."""
        return {
            "narrative_phrases": [
                r"我們認為",
                r"從.*角度來看",
                r"似乎",
                r"大約",
                r"基本上"
            ],
            "fuzzy_semantics": [
                r"大致完成",
                r"應該沒問題",
                r"差不多",
                r"可能"
            ],
            "fictional_completion": [
                r"已完成",
                r"已修復",
                r"已部署",
                r"問題已解決",
                r"系統已恢復"
            ]
        }
    
    def scan_text(self, text: str, file_path: str) -> List[Dict]:
        """Scan text for violations."""
        violations = []
        
        for violation_type, patterns in self.violation_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, text, re.IGNORECASE)
                for match in matches:
                    violation = {
                        "type": violation_type,
                        "pattern": pattern,
                        "line_number": self._find_line_number(text, match.start()),
                        "position": match.start(),
                        "matched_text": match.group(),
                        "file_path": file_path,
                        "severity": self._determine_severity(violation_type)
                    }
                    violations.append(violation)
        
        return violations
    
    def _find_line_number(self, text: str, position: int) -> int:
        """Find line number for a given position."""
        return text[:position].count('\n') + 1
    
    def _determine_severity(self, violation_type: str) -> str:
        """Determine severity based on violation type."""
        severity_map = {
            "narrative_phrases": "LOW",
            "fuzzy_semantics": "MEDIUM",
            "fictional_completion": "HIGH"
        }
        return severity_map.get(violation_type, "MEDIUM")
    
    def scan_directory(self, directory: str) -> Dict[str, List[Dict]]:
        """Scan directory for violations."""
        all_violations = {}
        
        for file_path in Path(directory).rglob("*.md"):
            with open(file_path, 'r') as f:
                text = f.read()
            
            violations = self.scan_text(text, str(file_path))
            if violations:
                all_violations[str(file_path)] = violations
        
        return all_violations


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Enhanced Semantic Scanner")
    parser.add_argument("--directory", required=True, help="Directory to scan")
    parser.add_argument("--output", required=True, help="Output file path")
    parser.add_argument("--config", default="ecosystem/enforcement/semantic_config.json")
    
    args = parser.parse_args()
    
    scanner = EnhancedSemanticScanner(args.config)
    violations = scanner.scan_directory(args.directory)
    
    with open(args.output, 'w') as f:
        json.dump(violations, f, indent=2)
    
    print(f"Scanning complete. Violations found in {len(violations)} files.")
    print(f"Results saved to {args.output}")


if __name__ == "__main__":
    main()
```

### Phase 2: Classification Layer Setup

#### Step 2.1: Implement Severity Classifier

**File:** `ecosystem/enforcement/severity_classifier.py`

```python
#!/usr/bin/env python3
"""
Severity Classifier for Violations
Based on NIST SP 800-204D risk assessment
"""

from typing import Dict, List
from enum import Enum


class SeverityLevel(Enum):
    """Severity levels for violations."""
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class SeverityClassifier:
    """Classify violations by severity."""
    
    def __init__(self, rules_config: str):
        self.rules_config = self._load_rules(rules_config)
    
    def _load_rules(self, config_path: str) -> Dict:
        """Load severity rules from configuration."""
        return {
            "CRITICAL": {
                "description": "Blocks deployment, immediate fix required",
                "auto_fix_enabled": False,
                "requires_human_review": True,
                "time_to_fix_hours": 1
            },
            "HIGH": {
                "description": "High impact, should fix before next release",
                "auto_fix_enabled": True,
                "requires_confirmation": True,
                "time_to_fix_hours": 8
            },
            "MEDIUM": {
                "description": "Moderate impact, schedule fix",
                "auto_fix_enabled": True,
                "requires_confirmation": False,
                "time_to_fix_hours": 24
            },
            "LOW": {
                "description": "Minor impact, track for backlog",
                "auto_fix_enabled": True,
                "requires_confirmation": False,
                "time_to_fix_hours": 72
            }
        }
    
    def classify_violation(self, violation: Dict) -> Dict:
        """Classify a single violation."""
        # Apply severity rules based on violation type and context
        base_severity = self._determine_base_severity(violation)
        adjusted_severity = self._adjust_severity(base_severity, violation)
        
        return {
            "violation_id": violation.get("id"),
            "severity": adjusted_severity.value,
            "description": self.rules_config[adjusted_severity.value]["description"],
            "auto_fix_enabled": self.rules_config[adjusted_severity.value]["auto_fix_enabled"],
            "requires_human_review": self.rules_config[adjusted_severity.value]["requires_human_review"],
            "time_to_fix_hours": self.rules_config[adjusted_severity.value]["time_to_fix_hours"],
            "classification_timestamp": self._get_timestamp()
        }
    
    def _determine_base_severity(self, violation: Dict) -> SeverityLevel:
        """Determine base severity from violation."""
        violation_type = violation.get("type", "")
        
        if "security" in violation_type.lower():
            return SeverityLevel.CRITICAL
        elif "architecture" in violation_type.lower():
            return SeverityLevel.HIGH
        elif "quality" in violation_type.lower():
            return SeverityLevel.MEDIUM
        else:
            return SeverityLevel.LOW
    
    def _adjust_severity(self, base_severity: SeverityLevel, violation: Dict) -> SeverityLevel:
        """Adjust severity based on context."""
        # Adjust based on impact, frequency, etc.
        impact = violation.get("impact", "low")
        frequency = violation.get("frequency", "low")
        
        if impact == "critical" or frequency == "high":
            return SeverityLevel.CRITICAL
        elif impact == "high" or frequency == "medium":
            if base_severity != SeverityLevel.CRITICAL:
                return SeverityLevel.HIGH
        
        return base_severity
    
    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime
        return datetime.utcnow().isoformat() + "Z"
    
    def classify_violations(self, violations: List[Dict]) -> List[Dict]:
        """Classify multiple violations."""
        return [self.classify_violation(v) for v in violations]
```

### Phase 3: Remediation Layer Setup

#### Step 3.1: Implement Auto-Fix Engine

**File:** `ecosystem/enforcement/auto_fix_engine.py`

```python
#!/usr/bin/env python3
"""
Auto-Fix Engine for Violation Remediation
Based on Parasoft AI-Driven + OpsMx DevSecOps patterns
"""

import json
from typing import Dict, List, Optional
from pathlib import Path


class AutoFixEngine:
    """Automated fix generation engine."""
    
    def __init__(self, config_path: str):
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        self.safety_measures = self.config.get("safety_measures", {})
    
    def generate_fix(self, violation: Dict) -> Dict:
        """Generate fix for a violation."""
        if not self._should_auto_fix(violation):
            return {
                "status": "MANUAL_REVIEW_REQUIRED",
                "reason": "Violation requires human review",
                "violation_id": violation.get("id")
            }
        
        # Generate fix based on violation type
        fix = self._generate_fix_for_type(violation)
        
        # Generate rollback script
        rollback = self._generate_rollback_script(violation, fix)
        
        return {
            "status": "FIX_GENERATED",
            "fix": fix,
            "rollback_script": rollback,
            "requires_confirmation": self._requires_confirmation(violation),
            "violation_id": violation.get("id")
        }
    
    def _should_auto_fix(self, violation: Dict) -> bool:
        """Determine if violation should be auto-fixed."""
        severity = violation.get("severity", "MEDIUM")
        auto_fix_enabled = self.safety_measures.get("auto_fix_enabled", {}).get(severity, True)
        
        return auto_fix_enabled
    
    def _requires_confirmation(self, violation: Dict) -> bool:
        """Determine if fix requires confirmation."""
        severity = violation.get("severity", "MEDIUM")
        return self.safety_measures.get("requires_confirmation", {}).get(severity, False)
    
    def _generate_fix_for_type(self, violation: Dict) -> Dict:
        """Generate fix based on violation type."""
        violation_type = violation.get("type", "")
        
        if "narrative" in violation_type.lower():
            return self._fix_narrative_violation(violation)
        elif "naming" in violation_type.lower():
            return self._fix_naming_violation(violation)
        elif "security" in violation_type.lower():
            return self._fix_security_violation(violation)
        else:
            return self._fix_generic_violation(violation)
    
    def _fix_narrative_violation(self, violation: Dict) -> Dict:
        """Fix narrative violations."""
        original_text = violation.get("matched_text", "")
        file_path = violation.get("file_path")
        line_number = violation.get("line_number")
        
        # Replace narrative phrase with factual statement
        replacements = {
            "我們認為": "分析結果顯示",
            "從...角度來看": "基於",
            "似乎": "資料指出",
            "大約": "約",
            "基本上": "具體來說"
        }
        
        for old, new in replacements.items():
            if old in original_text:
                new_text = original_text.replace(old, new)
                return {
                    "type": "text_replacement",
                    "file_path": file_path,
                    "line_number": line_number,
                    "original_text": original_text,
                    "new_text": new_text,
                    "reason": "Replace narrative phrase with factual statement"
                }
        
        return {
            "type": "manual_review",
            "reason": "No automatic replacement available"
        }
    
    def _fix_naming_violation(self, violation: Dict) -> Dict:
        """Fix naming violations."""
        old_name = violation.get("current_name")
        suggested_name = violation.get("suggested_name")
        file_path = violation.get("file_path")
        
        return {
            "type": "naming_refactor",
            "file_path": file_path,
            "old_name": old_name,
            "new_name": suggested_name,
            "scope": violation.get("scope", "file"),
            "reason": "Update naming to comply with conventions"
        }
    
    def _fix_security_violation(self, violation: Dict) -> Dict:
        """Fix security violations."""
        return {
            "type": "security_patch",
            "severity": "HIGH",
            "requires_manual_review": True,
            "suggestion": "Review security fix carefully before applying",
            "reference": violation.get("cve_reference", "")
        }
    
    def _fix_generic_violation(self, violation: Dict) -> Dict:
        """Fix generic violations."""
        return {
            "type": "manual_review",
            "reason": "Generic violation requires manual review"
        }
    
    def _generate_rollback_script(self, violation: Dict, fix: Dict) -> Dict:
        """Generate rollback script for fix."""
        return {
            "type": "rollback",
            "fix_id": fix.get("fix_id", ""),
            "original_state": {
                "file_path": violation.get("file_path"),
                "original_text": violation.get("matched_text")
            },
            "rollback_commands": [
                f"git checkout {violation.get('file_path')}",
                "Apply manual backup"
            ],
            "generated_at": self._get_timestamp()
        }
    
    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime
        return datetime.utcnow().isoformat() + "Z"
```

### Phase 4: Integration Layer Setup

#### Step 4.1: Implement CI/CD Integration

**File:** `.github/workflows/violation_enforcement.yml`

```yaml
name: Violation Enforcement

on:
  pull_request:
    branches: [main, develop]
  push:
    branches: [main, develop]
  workflow_dispatch:

jobs:
  detect_violations:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Run semantic scanner
        run: |
          python ecosystem/tools/enhanced_semantic_scanner.py \
            --directory . \
            --output violations_report.json
      
      - name: Classify violations
        run: |
          python ecosystem/enforcement/classify_violations.py \
            --input violations_report.json \
            --output classified_violations.json
      
      - name: Generate fixes
        if: contains(needs.*.outputs.result, 'VIOLATIONS_FOUND')
        run: |
          python ecosystem/enforcement/generate_fixes.py \
            --input classified_violations.json \
            --output fix_suggestions.json
      
      - name: Apply fixes (dry run)
        run: |
          python ecosystem/enforcement/apply_fixes.py \
            --input fix_suggestions.json \
            --mode dry-run
      
      - name: Upload violation reports
        uses: actions/upload-artifact@v3
        with:
          name: violation-reports
          path: |
            violations_report.json
            classified_violations.json
            fix_suggestions.json
      
      - name: Block PR on critical violations
        if: contains(needs.*.outputs.result, 'CRITICAL_VIOLATION')
        run: exit 1
```

#### Step 4.2: Service Mesh Integration (Istio)

**File:** `ecosystem/integration/istio/policy-enforcement.yaml`

```yaml
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata:
  name: governance-policy-enforcement
  namespace: default
spec:
  selector:
    matchLabels:
      app: machine-native-ops
  action: ALLOW
  rules:
    - from:
        - source:
            requestPrincipals: ["*"]
      to:
        - operation:
            methods: ["GET", "POST", "PUT", "DELETE"]
      when:
        - key: request.headers[governance-compliance]
          values: ["true"]
    - from:
        - source:
            requestPrincipals: ["*"]
      to:
        - operation:
            methods: ["*"]
      when:
        - key: request.headers[governance-token]
          values:
            - VALID_GOVERNANCE_TOKEN
```

---

## Code Examples

### Example 1: Complete Violation Remediation Workflow

```python
#!/usr/bin/env python3
"""
Complete Violation Remediation Workflow
End-to-end example from detection to fix application
"""

import json
from pathlib import Path


class ViolationRemediationWorkflow:
    """Complete workflow for violation remediation."""
    
    def __init__(self):
        self.steps = [
            "detect_violations",
            "classify_violations",
            "analyze_impact",
            "generate_fixes",
            "validate_fixes",
            "obtain_approval",
            "apply_fixes",
            "verify_fixes",
            "capture_evidence",
            "notify_stakeholders"
        ]
    
    def execute(self, source_directory: str) -> Dict:
        """Execute complete workflow."""
        workflow_result = {
            "workflow_id": self._generate_workflow_id(),
            "status": "STARTED",
            "steps_completed": [],
            "violations_found": 0,
            "fixes_applied": 0,
            "evidence_chain": []
        }
        
        try:
            # Step 1: Detect violations
            violations = self._detect_violations(source_directory)
            workflow_result["steps_completed"].append("detect_violations")
            workflow_result["violations_found"] = len(violations)
            
            if not violations:
                workflow_result["status"] = "COMPLETED_NO_VIOLATIONS"
                return workflow_result
            
            # Step 2: Classify violations
            classified = self._classify_violations(violations)
            workflow_result["steps_completed"].append("classify_violations")
            
            # Step 3: Analyze impact
            impact_analysis = self._analyze_impact(classified)
            workflow_result["steps_completed"].append("analyze_impact")
            
            # Step 4: Generate fixes
            fixes = self._generate_fixes(classified, impact_analysis)
            workflow_result["steps_completed"].append("generate_fixes")
            
            # Step 5: Validate fixes
            validation_results = self._validate_fixes(fixes)
            workflow_result["steps_completed"].append("validate_fixes")
            
            # Step 6: Obtain approval (if needed)
            approvals = self._obtain_approvals(fixes, validation_results)
            workflow_result["steps_completed"].append("obtain_approval")
            
            # Step 7: Apply fixes
            applied_fixes = self._apply_fixes(fixes, approvals)
            workflow_result["steps_completed"].append("apply_fixes")
            workflow_result["fixes_applied"] = len(applied_fixes)
            
            # Step 8: Verify fixes
            verification_results = self._verify_fixes(applied_fixes)
            workflow_result["steps_completed"].append("verify_fixes")
            
            # Step 9: Capture evidence
            evidence = self._capture_evidence(workflow_result)
            workflow_result["steps_completed"].append("capture_evidence")
            workflow_result["evidence_chain"] = evidence
            
            # Step 10: Notify stakeholders
            self._notify_stakeholders(workflow_result)
            workflow_result["steps_completed"].append("notify_stakeholders")
            
            workflow_result["status"] = "COMPLETED"
            
        except Exception as e:
            workflow_result["status"] = "FAILED"
            workflow_result["error"] = str(e)
        
        return workflow_result
    
    def _generate_workflow_id(self) -> str:
        """Generate unique workflow ID."""
        import uuid
        from datetime import datetime
        return f"workflow-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:8]}"
    
    def _detect_violations(self, source_directory: str) -> List[Dict]:
        """Detect violations in source directory."""
        # Implementation would call detection layer
        return []
    
    def _classify_violations(self, violations: List[Dict]) -> List[Dict]:
        """Classify violations by severity."""
        # Implementation would call classification layer
        return []
    
    def _analyze_impact(self, violations: List[Dict]) -> Dict:
        """Analyze impact of violations."""
        # Implementation would call impact analyzer
        return {}
    
    def _generate_fixes(self, violations: List[Dict], impact: Dict) -> List[Dict]:
        """Generate fixes for violations."""
        # Implementation would call auto-fix engine
        return []
    
    def _validate_fixes(self, fixes: List[Dict]) -> List[Dict]:
        """Validate fixes before application."""
        # Implementation would call fix validator
        return []
    
    def _obtain_approvals(self, fixes: List[Dict], validation: List[Dict]) -> Dict:
        """Obtain approvals for fixes."""
        # Implementation would check if approval needed and obtain it
        return {}
    
    def _apply_fixes(self, fixes: List[Dict], approvals: Dict) -> List[Dict]:
        """Apply approved fixes."""
        # Implementation would apply fixes
        return []
    
    def _verify_fixes(self, fixes: List[Dict]) -> List[Dict]:
        """Verify that fixes are effective."""
        # Implementation would verify fixes
        return []
    
    def _capture_evidence(self, workflow_result: Dict) -> List[Dict]:
        """Capture evidence of workflow execution."""
        # Implementation would capture all evidence
        return []
    
    def _notify_stakeholders(self, workflow_result: Dict):
        """Notify stakeholders of workflow completion."""
        # Implementation would send notifications
        pass


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Complete Violation Remediation Workflow")
    parser.add_argument("--directory", required=True, help="Source directory to remediate")
    parser.add_argument("--output", required=True, help="Output workflow result")
    
    args = parser.parse_args()
    
    workflow = ViolationRemediationWorkflow()
    result = workflow.execute(args.directory)
    
    with open(args.output, 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"Workflow completed: {result['status']}")
    print(f"Violations found: {result['violations_found']}")
    print(f"Fixes applied: {result['fixes_applied']}")


if __name__ == "__main__":
    main()
```

---

## Integration Examples

### Example 2: GitHub Actions Integration

See `.github/workflows/violation_enforcement.yml` above.

### Example 3: Service Mesh Integration with Istio

See `ecosystem/integration/istio/policy-enforcement.yaml` above.

### Example 4: API Gateway Integration (Kong)

**File:** `ecosystem/integration/kong/governance-plugin.lua`

```lua
-- Governance Plugin for Kong
-- Enforces governance policies at API gateway level

local governance_plugin = {
  PRIORITY = 1000,
  VERSION = "1.0.0",
}

function governance_plugin:access(config)
  -- Check governance compliance token
  local governance_token = kong.request.get_header("Governance-Token")
  
  if not governance_token or governance_token ~= config.expected_token then
    return kong.response.error(403, {
      message = "Governance compliance required",
      error = "INVALID_GOVERNANCE_TOKEN"
    })
  end
  
  -- Check if request is from approved governance-compliant system
  local source_system = kong.request.get_header("Source-System")
  if source_system and not config.approved_systems[source_system] then {
    return kong.response.error(403, {
      message = "Source system not approved",
      error = "UNAPPROVED_SYSTEM"
    })
  }
  
  -- Log governance enforcement
  kong.log.notice("Governance policy enforced for request: ",
                 kong.request.get_method(), " ", kong.request.get_path())
end

return governance_plugin
```

---

## Testing Strategy

### Unit Tests

```python
# tests/test_severity_classifier.py

import unittest
from ecosystem.enforcement.severity_classifier import SeverityClassifier, SeverityLevel


class TestSeverityClassifier(unittest.TestCase):
    """Test severity classifier."""
    
    def setUp(self):
        self.classifier = SeverityClassifier("ecosystem/enforcement/rules_config.json")
    
    def test_classify_security_violation(self):
        """Test classification of security violation."""
        violation = {
            "id": "SEC-001",
            "type": "security_vulnerability",
            "impact": "critical"
        }
        
        result = self.classifier.classify_violation(violation)
        
        self.assertEqual(result["severity"], "CRITICAL")
        self.assertFalse(result["auto_fix_enabled"])
        self.assertTrue(result["requires_human_review"])
    
    def test_classify_narrative_violation(self):
        """Test classification of narrative violation."""
        violation = {
            "id": "NAR-001",
            "type": "narrative_phrase",
            "impact": "low"
        }
        
        result = self.classifier.classify_violation(violation)
        
        self.assertEqual(result["severity"], "LOW")
        self.assertTrue(result["auto_fix_enabled"])


if __name__ == "__main__":
    unittest.main()
```

### Integration Tests

```python
# tests/integration/test_violation_workflow.py

import unittest
import json
from pathlib import Path
from ecosystem.enforcement.violation_remediation_workflow import ViolationRemediationWorkflow


class TestViolationWorkflow(unittest.TestCase):
    """Test violation remediation workflow."""
    
    def setUp(self):
        self.workflow = ViolationRemediationWorkflow()
        self.test_directory = Path("tests/fixtures/sample_violations")
    
    def test_workflow_execution(self):
        """Test complete workflow execution."""
        result = self.workflow.execute(str(self.test_directory))
        
        self.assertIn("status", result)
        self.assertIn("steps_completed", result)
        self.assertIn("violations_found", result)
    
    def test_workflow_with_no_violations(self):
        """Test workflow with no violations."""
        clean_directory = Path("tests/fixtures/clean_code")
        result = self.workflow.execute(str(clean_directory))
        
        self.assertEqual(result["status"], "COMPLETED_NO_VIOLATIONS")
        self.assertEqual(result["violations_found"], 0)


if __name__ == "__main__":
    unittest.main()
```

---

## Deployment Checklist

### Pre-Deployment

- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] Code review completed
- [ ] Security scan passed
- [ ] Performance benchmarks met
- [ ] Documentation updated
- [ ] Rollback plan prepared
- [ ] Monitoring configured

### Deployment

- [ ] Deploy to development environment
- [ ] Verify functionality in development
- [ ] Deploy to staging environment
- [ ] Verify functionality in staging
- [ ] Run full test suite
- [ ] Obtain final approval
- [ ] Deploy to production
- [ ] Verify production deployment

### Post-Deployment

- [ ] Monitor logs for errors
- [ ] Verify all integrations working
- [ ] Check performance metrics
- [ ] Validate compliance reports
- [ ] Notify stakeholders
- [ ] Document deployment
- [ ] Update runbook

---

## Success Metrics

| Metric | Target | Current |
|--------|--------|---------|
| Violation Detection Rate | > 95% | TBD |
| False Positive Rate | < 5% | TBD |
| Auto-Fix Success Rate | > 90% | TBD |
| Time to Fix | < 30 minutes | TBD |
| Evidence Completeness | 100% | TBD |
| Traceability Accuracy | > 99% | TBD |

---

## Next Steps

1. Implement detection layer components
2. Set up classification layer
3. Build remediation engine
4. Configure CI/CD integration
5. Deploy service mesh policies
6. Set up monitoring and alerting
7. Run end-to-end testing
8. Deploy to production

---

**Document Version:** 1.0.0  
**Last Updated:** 2026-02-05T06:00:00Z  
**Governance Owner:** IndestructibleAutoOps