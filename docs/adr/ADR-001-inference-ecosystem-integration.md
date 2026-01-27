# GL Unified Charter Activated
# ADR-001: Inference Ecosystem Research Integration

## Status
Accepted

## Context
The repository includes comprehensive research artifacts in `research/open-source-inference-ecosystem/`. These assets need to be integrated into the AEP Engine documentation flow so that governance stakeholders can reference them without altering runtime execution or GL layer boundaries.

## Decision
Integrate the inference ecosystem research as documentation-only inputs mapped to the AEP Engine pipeline. The integration is documented in the architecture guide and referenced from the documentation portal while keeping runtime modules unchanged.

## Consequences
### Positive
- Provides a clear governance-aligned entry point for inference ecosystem research.
- Preserves existing AEP Engine pipeline semantics while enabling documentation ingestion.

### Negative
- Requires periodic documentation review to avoid stale research insights.
- Adds an additional documentation artifact to maintain across governance reviews.

## Alternatives Considered
| Alternative | Pros | Cons | Why Not Chosen |
| --- | --- | --- | --- |
| Embed research into runtime configs | Closer to execution pipeline | Risk of altering pipeline behavior | Violates documentation-only constraint |
| Keep research isolated in research folder only | No additional maintenance | Hard to discover and govern | Lacks governance traceability |

## GL Governance Impact
- **Layer**: GL10-29 (Operational) for ADR; GL30-49 (Execution) for integration guidance
- **Compliance**: No changes to sealed governance artifacts or runtime components
- **Gates**: Documentation compliance and semantic boundary checks only

