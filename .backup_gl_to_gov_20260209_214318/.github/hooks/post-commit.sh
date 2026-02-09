#!/bin/bash
# @GL-governed
# @GL-layer: GL30-49
# @GL-semantic: git-hook-post-commit
# @GL-audit-trail: ../../engine/governance/GL_SEMANTIC_ANCHOR.json

# GL Governance Post-Commit Hook
# Logs governance events to event stream

COMMIT_HASH=$(git rev-parse HEAD)
COMMIT_AUTHOR=$(git log -1 --format='%an')
COMMIT_TIMESTAMP=$(git log -1 --format='%ct')
TIMESTAMP_ISO=$(date -u -d "@$COMMIT_TIMESTAMP" +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -r "$COMMIT_TIMESTAMP" +%Y-%m-%dT%H:%M:%SZ)

EVENT_FILE="engine/.governance/governance-event-stream.jsonl"

# Ensure directory exists
mkdir -p "$(dirname "$EVENT_FILE")"

# Create governance event
EVENT=$(cat <<EOF
{
  "event_type": "commit",
  "event_id": "evt_$(uuidgen 2>/dev/null || echo $RANDOM)",
  "timestamp": "$TIMESTAMP_ISO",
  "charter_version": "2.0.0",
  "execution_chain": ["pre-commit", "commit", "post-commit"],
  "data": {
    "commit_hash": "$COMMIT_HASH",
    "author": "$COMMIT_AUTHOR",
    "commit_timestamp": "$COMMIT_TIMESTAMP",
    "governance_status": "validated"
  }
}
EOF
)

# Append event to stream
echo "$EVENT" >> "$EVENT_FILE"

echo "✅ Governance event logged to event stream"
exit 0