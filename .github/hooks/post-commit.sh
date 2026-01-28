#!/bin/bash
# @GL-governed
# @GL-layer: GL10-29
# @GL-semantic: git-hook-post-commit-event-logging
# @GL-audit-trail: ../../engine/governance/GL_SEMANTIC_ANCHOR.json

# Log governance event to event stream
COMMIT_HASH=$(git rev-parse HEAD)
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
EVENT_TYPE="post-commit-validation"

EVENT=$(cat <<EOF
{
  "timestamp": "$TIMESTAMP",
  "event_type": "$EVENT_TYPE",
  "commit_hash": "$COMMIT_HASH",
  "governance_charter_version": "2.0.0",
  "status": "completed"
}
EOF
)

echo "$EVENT" >> engine/.governance/governance-event-stream.jsonl