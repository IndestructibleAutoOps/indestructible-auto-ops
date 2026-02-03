#!/usr/bin/env python3
import sys
sys.path.insert(0, '.')

from ecosystem.enforcers.role_executor import RoleExecutor, DateTimeEncoder
import json
import asyncio

async def test():
    try:
        print("Creating executor...")
        executor = RoleExecutor()
        
        print("Executing command...")
        result = await executor.execute('@role ecosystem.validator validate test.json')
        
        print("Converting to JSON...")
        output = json.dumps({
            'role_id': result.role_id,
            'invocation_id': result.invocation_id,
            'status': result.status,
            'timestamp': result.timestamp,
            'duration_ms': result.duration_ms,
            'result': result.result,
            'metadata': result.metadata
        }, indent=2, cls=DateTimeEncoder)
        
        print(output)
        return output
    except Exception as e:
        import traceback
        print(f"ERROR: {e}")
        traceback.print_exc()
        return None

if __name__ == "__main__":
    result = asyncio.run(test())
    if result:
        print("\nTest successful!")
    else:
        print("\nTest failed!")
        sys.exit(1)