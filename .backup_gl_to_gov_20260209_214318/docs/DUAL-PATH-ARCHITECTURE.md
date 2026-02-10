# Dual-Path Retrieval + Arbitration Reasoning Architecture

## Overview

The Dual-Path Retrieval + Arbitration Reasoning system is the core reasoning component of MNGA (Machine Native Governance Architecture). It implements a sophisticated decision-making process that combines internal and external knowledge sources through intelligent arbitration.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        User Request                             │
│                    "How to implement async task processing?"    │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Task Analysis Layer                          │
│  • Classify task type                                           │
│  • Extract context and requirements                              │
│  • Identify relevant knowledge domains                          │
└────────────────┬────────────────────────────────────────────────┘
                 │
         ┌───────┴───────┐
         │               │
         ▼               ▼
┌─────────────────┐ ┌─────────────────┐
│  Internal Path  │ │  External Path  │
└─────────────────┘ └─────────────────┘
         │                   │
         ▼                   ▼
┌─────────────────┐ ┌─────────────────┐
│ Vector Search   │ │  Web Search API  │
│ (ChromaDB)      │ │  (Bing/Google)   │
└────────┬────────┘ └────────┬────────┘
         │                   │
         ▼                   ▼
┌─────────────────┐ ┌─────────────────┐
│ Knowledge Graph │ │  Domain Filter  │
│ (Neo4j)         │ │  (Allowed URLs) │
└────────┬────────┘ └────────┬────────┘
         │                   │
         └─────────┬─────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Arbitration Layer                          │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Rule Engine                                            │   │
│  │  • HIGH_PRIORITY_MODULE_API → INTERNAL                  │   │
│  │  • SECURITY_VULNERABILITY_FIX → EXTERNAL                │   │
│  │  • DEPENDENCY_VERSION_UPDATE → HYBRID                   │   │
│  │  • CODE_STYLE_PREFERENCE → INTERNAL                     │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Confidence-Based Strategy                               │   │
│  │  • Internal confidence > 0.8 → Use internal              │   │
│  │  • External confidence > 0.85 → Use external            │   │
│  │  • Similar confidence (< 0.1 diff) → Hybrid             │   │
│  └─────────────────────────────────────────────────────────┘   │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Decision Output                            │
│                                                                 │
│  • Final answer (INTERNAL / EXTERNAL / HYBRID)                 │
│  • Reasoning explanation                                       │
│  • Confidence scores                                           │
│  • Source citations                                            │
│  • Risk assessment                                             │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Traceability Engine                           │
│                                                                 │
│  • Complete audit trail (actor, action, resource, result)      │
│  • RFC3339 UTC timestamps                                     │
│  • Evidence links and checksums                                │
│  • JSON/JSONL/Markdown export                                 │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Feedback Loop                                │
│                                                                 │
│  • Collect user feedback (ACCEPT/REJECT/MODIFY)                │
│  • Analyze patterns and trends                                 │
│  • Optimize confidence thresholds                              │
│  • Suggest rule adjustments                                    │
└─────────────────────────────────────────────────────────────────┘
```

## Components

### 1. Internal Retrieval Engine

**Purpose**: Search internal knowledge sources (code, documentation, policies, history)

**Key Features**:
- Vector-based semantic search using ChromaDB
- Knowledge graph queries using Neo4j
- Multi-layer indexing (symbol, call, semantic graphs)
- Context-aware search with depth control

**Implementation**: `ecosystem/reasoning/dual-path/internal/retrieval.py`

**Sources**:
```yaml
code:
  - Python, JavaScript, Go, TypeScript files
  - Index with embeddings
  
documentation:
  - Markdown files
  - Full-text search
  
governance:
  - YAML contracts
  - Highest priority
  
history:
  - Git commits
  - Issue discussions
  - Design decisions
```

### 2. External Retrieval Engine

**Purpose**: Search external knowledge sources (official docs, best practices)

**Key Features**:
- Web search API integration (Bing/Google)
- Domain filtering (allowlist)
- Result caching with TTL
- Confidence-based ranking

**Implementation**: `ecosystem/reasoning/dual-path/external/retrieval.py`

**Allowed Domains**:
```yaml
- docs.python.org
- go.dev
- nodejs.org
- developer.mozilla.org
- kubernetes.io
- istio.io
- prometheus.io
- grafana.com
```

### 3. Knowledge Graph

**Purpose**: Build and query multi-layer code structure graph

**Layers**:
```
L1: Symbol Graph    - Functions, classes, variables
L2: Call Graph      - Function call relationships
L3: Semantic Graph  - High-level concepts
```

**Features**:
- AST parsing with tree-sitter
- Dependency analysis
- Impact analysis for refactoring
- Context queries with upstream/downstream

**Implementation**: `ecosystem/reasoning/dual-path/internal/knowledge_graph.py`

### 4. Arbitrator

**Purpose**: Make decisions between internal and external results

**Decision Process**:
1. Apply rule engine (highest priority)
2. Use confidence-based strategy (fallback)
3. Merge results for hybrid decisions
4. Generate explanation with reasoning chain

**Rules**:
```python
HIGH_PRIORITY_MODULE_API:
  - Core modules (gov-platform-services, gov-execution-runtime)
  - Internal confidence > 0.8
  → Use INTERNAL

SECURITY_VULNERABILITY_FIX:
  - Security category
  - Vulnerability fix type
  → Use EXTERNAL

DEPENDENCY_VERSION_UPDATE:
  - Version mismatch
  → Use HYBRID (require review)

CODE_STYLE_PREFERENCE:
  - Style type
  - Internal confidence > 0.7
  → Use INTERNAL
```

**Implementation**: `ecosystem/reasoning/dual-path/arbitration/arbitrator.py`

### 5. Traceability Engine

**Purpose**: Track complete reasoning process for audit

**Audit Fields**:
- actor, action, resource, result
- hash, version, requestId, correlationId
- ip, userAgent
- timestamp (RFC3339 UTC)

**Output Formats**:
- JSON
- JSONL (for log aggregation)
- Markdown (human-readable)

**Implementation**: `ecosystem/reasoning/traceability/traceability.py`

### 6. Feedback Loop

**Purpose**: Learn from user decisions to improve system

**Feedback Types**:
- ACCEPT - User accepted suggestion
- REJECT - User rejected suggestion
- MODIFY - User modified suggestion
- IGNORE - User ignored suggestion

**Analysis**:
- Acceptance rate tracking
- Rejection reason analysis
- Rule performance metrics
- Threshold optimization

**Implementation**: `ecosystem/reasoning/traceability/feedback.py`

## Usage

### Basic Usage

```python
from platforms.gl.platform_assistant.orchestration.pipeline import ReasoningPipeline

# Initialize pipeline
pipeline = ReasoningPipeline()

# Handle request
response = pipeline.handle_request(
    task_spec="How should I implement async task processing in Python?",
    context={
        "sources": ["code", "documentation"],
        "domains": ["docs.python.org"]
    },
    user_id="user123"
)

# Access results
print(f"Request ID: {response['request_id']}")
print(f"Final Answer: {response['final_answer']}")
print(f"Decision: {response['decision']['decision']}")
```

### Submit Feedback

```python
# Submit user feedback
pipeline.submit_feedback(
    request_id=response['request_id'],
    feedback_type="ACCEPT",
    reason="Helpful and accurate",
    user_id="user123"
)
```

### Get Metrics

```python
# Get pipeline metrics
metrics = pipeline.get_metrics()
print(f"Total requests: {metrics['total_requests']}")
print(f"Decision distribution: {metrics['decision_distribution']}")
```

## Configuration

### Dual-Path Spec

Edit `ecosystem/contracts/reasoning/dual_path_spec.yaml`:

```yaml
spec:
  internal_retrieval:
    vector_store:
      type: chromadb
      embedding_model: text-embedding-3-small
    knowledge_graph:
      type: neo4j
      uri: bolt://localhost:7687
      
  external_retrieval:
    web_search:
      provider: bing
      max_results: 10
    domain_filter:
      enabled: true
      allowed_domains:
        - docs.python.org
        - kubernetes.io
        
  arbitration:
    default_strategy: confidence_based
    confidence_threshold:
      internal: 0.8
      external: 0.85
      hybrid: 0.75
```

### Arbitration Rules

Edit rules in `ecosystem/reasoning/dual-path/arbitration/rules/`:
- `security.yaml` - Security-related rules
- `api.yaml` - API-related rules
- `dependency.yaml` - Dependency rules

## Integration with MNGA

### MNGA Layer 6

The Dual-Path Retrieval + Arbitration system is **MNGA Layer 6 (Reasoning)**:

```
Layer 0: Language      ← Prompt templates, parsing
Layer 1: Format        ← JSON Schema, YAML config
Layer 2: Semantic      ← Knowledge alignment
Layer 3: Index         ← Vector indices, search
Layer 4: Topology      ← Knowledge graphs
Layer 5: Enforcement   ← Policy execution
Layer 6: Reasoning     ← Dual-path + arbitration ⭐ YOU ARE HERE
Layer 7: Monitoring    ← Traceability, audit
```

### Integration Points

1. **Governance Enforcement**: `ecosystem/enforce.py` calls reasoning for decisions
2. **Auto-Fix Workflow**: `.github/workflows/auto-fix.yaml` uses reasoning for fixes
3. **Naming Governance**: `.github/workflows/naming-governance.yaml` applies arbitration
4. **CI Pipeline**: `.github/workflows/ci-pipeline.yaml` validates reasoning

## Monitoring

### Metrics

Track these metrics:
- Total requests
- Decision distribution (INTERNAL/EXTERNAL/HYBRID/REJECT)
- Confidence score distribution
- Acceptance rate
- Latency (retrieval, arbitration, total)

### Alerts

Configure alerts in `.config/prometheus/`:
- High rejection rate
- Low acceptance rate
- High latency
- Confidence threshold breaches

### Dashboards

View dashboards in Grafana:
- Dual-path performance
- Arbitration decisions
- Feedback analysis
- System health

## Best Practices

### For Developers

1. **Prefer Internal**: Always check internal knowledge first for project-specific patterns
2. **Validate External**: Verify external solutions against project requirements
3. **Provide Context**: Include relevant context (sources, domains) in requests
4. **Submit Feedback**: Always submit feedback to improve the system
5. **Review Traces**: Check traceability reports for audit and debugging

### For Operators

1. **Monitor Confidence**: Watch for low confidence decisions
2. **Review Feedback**: Analyze feedback patterns for system improvements
3. **Tune Thresholds**: Adjust confidence thresholds based on acceptance rates
4. **Update Rules**: Add or modify arbitration rules as needed
5. **Maintain Knowledge**: Keep internal indexes and knowledge graph up to date

## Troubleshooting

### Common Issues

**Issue**: Low confidence from both paths
**Solution**: 
- Check if question is specific enough
- Verify internal index is up to date
- Review domain filter configuration

**Issue**: Wrong decision (e.g., internal when external was better)
**Solution**: 
- Submit feedback with reason
- Review arbitration rules
- Adjust confidence thresholds

**Issue**: Slow response time
**Solution**: 
- Check vector database performance
- Optimize knowledge graph queries
- Increase cache size

## Future Enhancements

### Planned Features

1. **Agent Integration**: Enable agents to perform tasks, not just answer questions
2. **Multi-Modal**: Support for images, videos, and audio
3. **Streaming**: Real-time response streaming
4. **Personalization**: Learn user preferences over time
5. **Collaborative**: Share knowledge across teams

### Research Areas

1. **Advanced Arbitration**: Machine learning-based arbitration
2. **Conflict Resolution**: Sophisticated conflict handling
3. **Confidence Calibration**: Better confidence score estimation
4. **Knowledge Fusion**: Advanced internal/external knowledge merging

## References

- [MNGA Architecture](./ARCHITECTURE.md)
- [API Documentation](./API.md)
- [Runbooks](./runbooks/)
- [Governance Policies](../ecosystem/contracts/governance/)

---

Last Updated: 2026-02-03