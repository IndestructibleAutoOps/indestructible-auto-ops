# ADR-002: Pull-All-Files Retrieval

## Status
Proposed

## Context
Issue #326 requests a "pull all files" capability for the File Organizer system. Current APIs
paginate results by default to avoid large payloads and resource pressure. A governance-aligned
approach is needed to retrieve full file inventories without changing existing behavior.

## Decision
Introduce a dedicated pull-all-files mode or export endpoint that performs chunked retrieval and
records access events. Existing paginated endpoints remain unchanged to preserve compatibility.

## Consequences
### Positive
- Enables full inventory export for analytics and audits.
- Preserves default pagination behavior for existing consumers.
- Provides a clear governance trail for bulk access.

### Negative
- Requires additional authorization and monitoring for bulk usage.
- Adds a new operational path to maintain.

## Alternatives Considered
| Alternative | Pros | Cons | Why Not Chosen |
| --- | --- | --- | --- |
| Expand default `/api/files` to return all rows | Minimal API change | Breaks pagination defaults, large payload risk | Violates performance and safety goals |
| Require manual DB access | Zero API changes | Bypasses governance controls | Lacks auditability |
| Add export path with chunked retrieval | Safe and explicit | Additional endpoint | Selected for safety and governance alignment |

## GL Governance Impact
- **Layer**: GL10-29 (Operational) for decision record; GL30-49 (Execution) for API design
- **Compliance**: No changes to sealed governance artifacts or runtime schemas
- **Gates**: Requires access logging and authorization checks for bulk retrieval
