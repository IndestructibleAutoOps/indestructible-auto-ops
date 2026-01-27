# Autonomy Level Classification Framework

**Version**: 1.0.0  
**Status**: Active  
**Last Updated**: 2026-01-18

---

## Overview

This framework defines the criteria and scoring system for classifying modules and components according to their autonomy levels (L1-L5). The framework enables objective assessment of automation sophistication and guides progression towards higher autonomy.

---

## Autonomy Levels Definition

### L1: Basic Automation
**Characteristics**:
- Manual configuration required
- Reactive operations only
- Human intervention for most decisions
- Simple rule-based logic
- No self-adaptation

**Example Operations**:
- File I/O with manual paths
- Fixed configuration loading
- Basic data validation
- Simple logging

**Human Intervention**: 80-100%

---

### L2: Conditional Automation
**Characteristics**:
- Basic decision-making with predefined conditions
- Limited self-configuration
- Some proactive monitoring
- Rule-based automation
- Minimal self-adaptation

**Example Operations**:
- Environment-based configuration selection
- Conditional workflow execution
- Basic error recovery
- Automated alerts

**Human Intervention**: 50-80%

---

### L3: Contextual Automation
**Characteristics**:
- Context-aware decision-making
- Self-configuration based on environment
- Proactive monitoring and optimization
- Learning from patterns
- Moderate self-adaptation

**Example Operations**:
- Dynamic resource allocation
- Intelligent retry strategies
- Pattern-based optimization
- Self-healing capabilities

**Human Intervention**: 20-50%

---

### L4: Cognitive Automation
**Characteristics**:
- Advanced AI/ML-based decision-making
- Comprehensive self-management
- Predictive analytics
- Autonomous optimization
- High self-adaptation

**Example Operations**:
- Predictive scaling
- Anomaly detection and remediation
- Intelligent workload distribution
- Self-optimization based on metrics

**Human Intervention**: 5-20%

---

### L5: Full Autonomy
**Characteristics**:
- Complete self-governance
- Autonomous goal achievement
- Self-evolution and improvement
- Multi-agent collaboration
- Continuous self-adaptation

**Example Operations**:
- Autonomous architecture evolution
- Self-directed learning and improvement
- Collaborative multi-agent systems
- Autonomous decision-making at all levels

**Human Intervention**: 0-5%

---

### Global Layer (GL): Cross-Cutting Governance
**Characteristics**:
- VETO authority over all levels
- Cross-module governance
- Security and compliance enforcement
- System-wide policy management
- Independent of autonomy progression

**Example Operations**:
- Security policy enforcement
- Compliance validation
- Global access control
- System-wide auditing

**Special Status**: Outside autonomy progression; always enforced

---

## Classification Criteria

### 1. Decision-Making (30 points)

| Level | Points | Criteria |
|-------|--------|----------|
| L1 | 0-6 | Hardcoded logic, no decision-making |
| L2 | 7-12 | Simple if/else conditions |
| L3 | 13-18 | Context-aware, rule-based decisions |
| L4 | 19-24 | ML/AI-driven decisions |
| L5 | 25-30 | Autonomous goal-directed decisions |

### 2. Self-Configuration (25 points)

| Level | Points | Criteria |
|-------|--------|----------|
| L1 | 0-5 | Manual configuration only |
| L2 | 6-10 | Environment-based config selection |
| L3 | 11-15 | Dynamic configuration adaptation |
| L4 | 16-20 | Predictive configuration optimization |
| L5 | 21-25 | Fully autonomous configuration management |

### 3. Monitoring & Response (20 points)

| Level | Points | Criteria |
|-------|--------|----------|
| L1 | 0-4 | Manual monitoring |
| L2 | 5-8 | Reactive alerts |
| L3 | 9-12 | Proactive monitoring with auto-response |
| L4 | 13-16 | Predictive monitoring and prevention |
| L5 | 17-20 | Autonomous self-healing and optimization |

### 4. Learning & Adaptation (15 points)

| Level | Points | Criteria |
|-------|--------|----------|
| L1 | 0-3 | No learning capability |
| L2 | 4-6 | Basic pattern recognition |
| L3 | 7-9 | Historical pattern learning |
| L4 | 10-12 | ML-based adaptive learning |
| L5 | 13-15 | Continuous self-improvement |

### 5. Error Handling (10 points)

| Level | Points | Criteria |
|-------|--------|----------|
| L1 | 0-2 | Fails immediately |
| L2 | 3-4 | Basic retry logic |
| L3 | 5-6 | Intelligent error recovery |
| L4 | 7-8 | Predictive error prevention |
| L5 | 9-10 | Autonomous error resolution |

**Total Score**: 100 points

---

## Classification Process

### Step 1: Component Assessment

For each component, evaluate against 5 criteria:

```yaml
component_assessment:
  component_name: "example-service"
  scores:
    decision_making: 18      # L3 level
    self_configuration: 15   # L3 level
    monitoring_response: 12  # L3 level
    learning_adaptation: 9   # L3 level
    error_handling: 6        # L3 level
  total_score: 60           # Average: L3
```

### Step 2: Score Mapping

| Total Score | Autonomy Level |
|-------------|----------------|
| 0-20 | L1 |
| 21-40 | L2 |
| 41-60 | L3 |
| 61-80 | L4 |
| 81-100 | L5 |

### Step 3: Module Classification

Module level = weighted average of component levels:

```python
module_level = sum(component_score * component_weight) / total_weight
```

Weights based on component criticality:
- Core components: 3x
- Supporting components: 2x
- Utility components: 1x

---

## Classification Script

### Usage

```bash
./scripts/classify-autonomy.py --module 01-core --output report.json
```

### Output Format

```json
{
  "module_id": "01-core",
  "autonomy_level": "L1-L2",
  "total_score": 35,
  "components": [
    {
      "name": "ServiceRegistry",
      "level": "L2",
      "score": 28,
      "breakdown": {
        "decision_making": 10,
        "self_configuration": 8,
        "monitoring_response": 6,
        "learning_adaptation": 2,
        "error_handling": 2
      }
    }
  ],
  "recommendations": [
    "Enhance decision-making with contextual awareness",
    "Implement adaptive configuration management",
    "Add proactive monitoring capabilities"
  ]
}
```

---

## Progression Guidelines

### From L1 to L2
1. Add conditional logic based on environment
2. Implement basic retry mechanisms
3. Add reactive monitoring and alerts
4. Enable environment-based configuration

### From L2 to L3
1. Implement context-aware decision-making
2. Add dynamic configuration adaptation
3. Enable proactive monitoring
4. Implement pattern-based learning
5. Add intelligent error recovery

### From L3 to L4
1. Integrate ML/AI for decision-making
2. Implement predictive analytics
3. Add autonomous optimization
4. Enable self-healing capabilities
5. Implement advanced anomaly detection

### From L4 to L5
1. Enable full autonomous goal-directed behavior
2. Implement multi-agent collaboration
3. Add continuous self-evolution
4. Enable autonomous architecture adaptation
5. Implement self-directed learning

---

## Validation Rules

### Dependency Constraints

1. **Minimum Dependency Level**:
   - A module's autonomy level must be ≥ all its dependencies
   - Exception: Global Layer can depend on any level

2. **Maximum Progression Jump**:
   - Modules can only increase by 2 levels at a time
   - Example: L1 → L3 allowed, L1 → L4 not allowed

3. **Consistency Check**:
   - All components within a module should be within 1 level of each other
   - Significant variance indicates refactoring needed

---

## Module Classification Results

### Current Classifications

| Module | Current Level | Score | Target Level | Priority |
|--------|--------------|-------|--------------|----------|
| 01-core | L1-L2 | 35 | L2-L3 | High |
| 02-intelligence | L2-L3 | 55 | L3-L4 | High |
| 03-governance | L3-L4 | 65 | L4 | Medium |
| 04-autonomous | L4-L5 | 75 | L5 | Low |
| 05-observability | L4-L5 | 72 | L5 | Low |
| 06-security | Global Layer | N/A | Global Layer | N/A |

---

## Metrics & Tracking

### Key Performance Indicators

1. **Overall Autonomy Score**: Average autonomy level across all modules
2. **Autonomy Coverage**: % of components classified
3. **Progression Rate**: Autonomy level improvements per quarter
4. **Human Intervention Ratio**: Actual human intervention vs. expected

### Target Metrics (2026)

- Overall Autonomy Score: L3.5
- Autonomy Coverage: 100%
- Progression Rate: +0.5 levels/quarter
- Human Intervention Ratio: <30%

---

## Governance Integration

### Policy Enforcement

The autonomy policy (`controlplane/governance/policies/autonomy.rego`) enforces:

1. **Minimum Level Requirement**: All modules must meet minimum threshold
2. **Dependency Validation**: Dependencies must have appropriate autonomy levels
3. **Progression Limits**: Maximum 2-level jumps
4. **Documentation Requirements**: All classifications must be documented

### Audit Trail

All autonomy level changes are tracked in:
- Module manifest version history
- Classification reports (timestamped)
- Governance audit logs

---

## Tools & Resources

### Classification Tools

- `scripts/classify-autonomy.py` - Automated classification script
- `scripts/validate-autonomy.py` - Validation and consistency checks
- `scripts/generate-autonomy-report.py` - Generate classification reports

### Documentation

- Module manifests: `controlplane/baseline/modules/*/module-manifest.yaml`
- Classification reports: `docs/autonomy/classification-reports/`
- Progression plans: `docs/autonomy/progression-plans/`

---

## References

- [Module Registry](../controlplane/baseline/modules/REGISTRY.yaml)
- [Autonomy Policy](../controlplane/governance/policies/autonomy.rego)
- [Research Verification Plan](../research_report_verification_plan.md)
- [Integration Guide](../docs/PHASE1_INTEGRATION_GUIDE.md)

---

*This framework is part of the MachineNativeOps governance system and is actively maintained.*  
*Last updated: 2026-01-18*
