@GL-governed
# Capability Definition Language (CDL)

## Overview

The Capability Definition Language (CDL) is a declarative language for defining capabilities in the GL Code Intelligence & Security Layer. It provides a standardized way to describe what a capability does, its inputs/outputs, dimensions, guarantees, and metadata.

## Core Concepts

### Capability

A **Capability** is the fundamental unit of the CDL. It represents a specific function that the Code Intelligence & Security Layer can perform.

**Key Properties:**
- `id`: Unique identifier (UUID)
- `name`: Human-readable name
- `version`: Semantic version (e.g., "1.0.0")
- `category`: Capability category (8 predefined categories)
- `description`: Detailed description of what the capability does

### Capability Categories

1. **deep-code-understanding**: Semantic analysis and code comprehension
2. **security-hardening**: Security vulnerability detection and fixing
3. **performance-optimization**: Code performance improvements
4. **architecture-refactoring**: Structural code improvements
5. **test-generation**: Automated test case creation
6. **documentation-synthesis**: Documentation generation
7. **dependency-analysis**: Dependency management and analysis
8. **vulnerability-detection**: Security vulnerability scanning

### Input Types

- `sourcecode`: Source code files
- `runtimetraces`: Execution traces
- `dependency-graph`: Dependency relationships
- `configuration`: Configuration files
- `metrics`: Performance metrics
- `logs`: Application logs
- `user-feedback`: User feedback and annotations
- `pattern-hints`: Pattern matching hints

### Output Types

- `semantic-model`: Semantic representation of code
- `architecture-map`: Architecture visualization
- `risk-profile`: Security and risk assessment
- `patch`: Code patch
- `refactored-code`: Refactored source code
- `test-cases`: Test suite
- `documentation`: Generated documentation
- `metrics`: Performance metrics
- `report`: Analysis report
- `visualization`: Visual representation

## Example Capability Definition

```typescript
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "SQL Injection Detector",
  "version": "1.0.0",
  "category": "security-hardening",
  "description": "Detects SQL injection vulnerabilities in code",
  "inputs": [
    {
      "id": "source-code",
      "type": "sourcecode",
      "description": "Source code to analyze",
      "required": true
    }
  ],
  "outputs": [
    {
      "id": "vulnerabilities",
      "type": "risk-profile",
      "description": "Detected SQL injection vulnerabilities",
      "format": "sarif"
    }
  ],
  "dimensions": {
    "precision": 0.95,
    "recall": 0.90,
    "f1-score": 0.92,
    "latency-ms": 500,
    "throughput-files-per-second": 10
  },
  "guarantees": [
    {
      "type": "no-false-positives",
      "description": "Zero false positive rate on known safe code"
    }
  ],
  "metadata": {
    "author": "GL Security Team",
    "created-at": "2026-01-29T00:00:00Z",
    "updated-at": "2026-01-29T00:00:00Z"
  },
  "evolution": {
    "generation": 1,
    "usage-count": 0,
    "success-rate": 1.0,
    "average-performance": 0.0
  }
}
```

## Validation Rules

Capabilities support validation rules for inputs:

- **regex**: Pattern matching with regular expressions
- **schema**: JSON schema validation
- **custom**: Custom validation functions
- **type-check**: Type checking

## Dimensions

Capabilities are measured along multiple dimensions:

- **precision**: Accuracy of positive predictions
- **recall**: Coverage of actual positives
- **f1-score**: Harmonic mean of precision and recall
- **latency-ms**: Execution time
- **throughput-files-per-second**: Processing speed

## Evolution Tracking

Every capability tracks its evolution:

- **generation**: Evolution generation number
- **usage-count**: Number of times used
- **success-rate**: Percentage of successful executions
- **average-performance**: Average performance score

## Best Practices

1. Use descriptive names and detailed descriptions
2. Define clear input/output contracts
3. Set realistic dimension targets
4. Track evolution for continuous improvement
5. Use UUIDs for capability IDs

## Version Compatibility

- CDL Version: 21.0.0
- Backward Compatible With: 20.x.x
- Breaking Changes: None