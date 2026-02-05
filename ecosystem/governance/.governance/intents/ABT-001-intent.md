# Intent Document: ABT-001

## Intent Statement
"When external API is unavailable (timeout > 5s), the system should:
 1. Detect unavailability within 5 seconds
 2. Switch to local cache
 3. Log GL event with type 'external_api_unavailable'
 4. NOT attempt auto-repair
 5. Return degraded response with cache_source header"


## Intent Boundaries
- Only cache data older than 1 hour
- Only serve read-only operations (GET, HEAD)
- Must not modify cached data
- Must not retry API without human approval

## Approval
- Approved by: governance_validator
- Approval timestamp: 2026-02-05T11:40:00Z
