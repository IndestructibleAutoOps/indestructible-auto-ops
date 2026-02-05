#!/usr/bin/env python3
"""
Event Stream Migration Tool
===========================

Migrates historical events to add:
- canonical_hash (RFC 8785 JCS canonicalization)
- hash_chain (event chain linking)
- era field

This is required for Era-1 sealing.
"""

import os
import sys
import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

sys.path.insert(0, '/workspace/ecosystem')
sys.path.insert(0, '/workspace')


class EventStreamMigrator:
    """Migrates event stream to add missing fields"""
    
    def __init__(self, workspace: str = "/workspace"):
        self.workspace = Path(workspace)
        self.event_stream_file = self.workspace / "ecosystem" / ".governance" / "event-stream.jsonl"
        self.backup_file = self.event_stream_file.with_suffix('.jsonl.backup')
        
        self.migrated_count = 0
        self.errors = []
        
    def migrate(self, dry_run: bool = False) -> Dict[str, Any]:
        """Migrate event stream to add missing fields"""
        print("🔄 Starting Event Stream Migration...")
        print(f"📁 Event Stream: {self.event_stream_file}")
        print(f"📁 Backup: {self.backup_file}")
        print()
        
        if not self.event_stream_file.exists():
            print(f"❌ Error: Event stream file not found: {self.event_stream_file}")
            return {"success": False, "error": "File not found"}
        
        # Create backup
        print("📦 Creating backup...")
        if not self.backup_file.exists():
            import shutil
            shutil.copy(self.event_stream_file, self.backup_file)
            print(f"✅ Backup created: {self.backup_file}")
        else:
            print(f"⚠️  Backup already exists, using existing: {self.backup_file}")
        
        # Read all events
        print(f"📖 Reading events...")
        events = []
        with open(self.event_stream_file, 'r') as f:
            for line_num, line in enumerate(f, 1):
                try:
                    event = json.loads(line.strip())
                    events.append(event)
                except Exception as e:
                    self.errors.append({
                        "line": line_num,
                        "error": str(e),
                        "line_content": line[:200]
                    })
        
        print(f"   Total events: {len(events)}")
        print(f"   Parse errors: {len(self.errors)}")
        print()
        
        # Migrate events
        print("🔧 Migrating events...")
        migrated_events = []
        added_canonical_hash = 0
        added_hash_chain = 0
        added_era = 0
        
        # Import canonicalization tool
        try:
            from ecosystem.tools.canonicalize import canonicalize_json
        except ImportError:
            print("❌ Error: Canonicalization tool not available")
            print("   Install: pip install rfc8785")
            return {"success": False, "error": "Canonicalization tool not available"}
        
        for i, event in enumerate(events):
            # Add era field if missing (default to 1 for historical events)
            if 'era' not in event:
                event['era'] = 1
                added_era += 1
            
            # Add canonical_hash if missing
            if 'canonical_hash' not in event:
                # Remove hash fields before canonicalizing (to avoid circular dependency)
                event_copy = event.copy()
                event_copy.pop('canonical_hash', None)
                event_copy.pop('hash_chain', None)
                
                try:
                    canonical_str = canonicalize_json(event_copy)
                    canonical_hash = hashlib.sha256(canonical_str.encode('utf-8')).hexdigest()
                    event['canonical_hash'] = canonical_hash
                    added_canonical_hash += 1
                except Exception as e:
                    print(f"⚠️  Warning: Failed to canonicalize event {i}: {e}")
            
            # Add hash_chain if missing
            if 'hash_chain' not in event:
                # Link to previous event
                if i > 0:
                    previous_event = migrated_events[i-1]
                    previous_canonical_hash = previous_event.get('canonical_hash', '')
                    hash_chain = {
                        "self": event.get('canonical_hash', ''),
                        "previous_event": previous_canonical_hash,
                        "previous_artifact": previous_event.get('artifact_hash', '')
                    }
                else:
                    hash_chain = {
                        "self": event.get('canonical_hash', ''),
                        "previous_event": None,
                        "previous_artifact": None
                    }
                
                event['hash_chain'] = hash_chain
                added_hash_chain += 1
            
            # Add canonicalization metadata
            if 'canonicalization_version' not in event:
                event['canonicalization_version'] = "1.0"
            if 'canonicalization_method' not in event:
                event['canonicalization_method'] = "JCS+LayeredSorting"
            
            migrated_events.append(event)
            self.migrated_count += 1
        
        print(f"   Migrated: {self.migrated_count}")
        print(f"   Added canonical_hash: {added_canonical_hash}")
        print(f"   Added hash_chain: {added_hash_chain}")
        print(f"   Added era: {added_era}")
        print()
        
        if dry_run:
            print("🔍 Dry run complete - no changes made")
            return {
                "success": True,
                "dry_run": True,
                "migrated_count": self.migrated_count,
                "added_canonical_hash": added_canonical_hash,
                "added_hash_chain": added_hash_chain,
                "added_era": added_era,
                "errors": self.errors
            }
        
        # Write migrated events
        print("💾 Writing migrated events...")
        with open(self.event_stream_file, 'w') as f:
            for event in migrated_events:
                f.write(json.dumps(event, ensure_ascii=False) + '\n')
        
        print(f"✅ Migration complete")
        print()
        
        return {
            "success": True,
            "dry_run": False,
            "migrated_count": self.migrated_count,
            "added_canonical_hash": added_canonical_hash,
            "added_hash_chain": added_hash_chain,
            "added_era": added_era,
            "errors": self.errors
        }
    
    def verify(self) -> Dict[str, Any]:
        """Verify migration by checking events"""
        print("🔍 Verifying migration...")
        
        events_missing_canonical_hash = 0
        events_missing_hash_chain = 0
        events_missing_era = 0
        total_events = 0
        
        with open(self.event_stream_file, 'r') as f:
            for line in f:
                event = json.loads(line.strip())
                total_events += 1
                
                if 'canonical_hash' not in event:
                    events_missing_canonical_hash += 1
                
                if 'hash_chain' not in event:
                    events_missing_hash_chain += 1
                
                if 'era' not in event:
                    events_missing_era += 1
        
        print(f"   Total events: {total_events}")
        print(f"   Missing canonical_hash: {events_missing_canonical_hash}")
        print(f"   Missing hash_chain: {events_missing_hash_chain}")
        print(f"   Missing era: {events_missing_era}")
        print()
        
        success = (
            events_missing_canonical_hash == 0 and
            events_missing_hash_chain == 0 and
            events_missing_era == 0
        )
        
        return {
            "success": success,
            "total_events": total_events,
            "events_missing_canonical_hash": events_missing_canonical_hash,
            "events_missing_hash_chain": events_missing_hash_chain,
            "events_missing_era": events_missing_era
        }


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Migrate event stream to add canonical_hash and hash_chain")
    parser.add_argument('--dry-run', action='store_true', help='Run migration without writing changes')
    parser.add_argument('--verify', action='store_true', help='Verify migration without running')
    
    args = parser.parse_args()
    
    migrator = EventStreamMigrator()
    
    if args.verify:
        result = migrator.verify()
    else:
        result = migrator.migrate(dry_run=args.dry_run)
        
        if result.get("success") and not args.dry_run:
            print("=" * 70)
            print("✅ Migration Successful")
            print("=" * 70)
            print(f"   Migrated: {result['migrated_count']} events")
            print(f"   Added canonical_hash: {result['added_canonical_hash']}")
            print(f"   Added hash_chain: {result['added_hash_chain']}")
            print(f"   Added era: {result['added_era']}")
            print("=" * 70)
            
            # Verify migration
            verification = migrator.verify()
            
            if verification['success']:
                print("✅ Verification Passed - All events have required fields")
                sys.exit(0)
            else:
                print("❌ Verification Failed - Some events still missing fields")
                sys.exit(1)


if __name__ == "__main__":
    main()