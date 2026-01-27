#!/usr/bin/env python3
import json

with open('security_audit_post_fix.json') as f:
    data = json.load(f)

critical = [f for f in data['findings'] if f['severity'] == 'critical']
print(f'Remaining CRITICAL findings: {len(critical)}\n')

for f in critical:
    print(f'{f["file"]}:{f["line"]}')
    print(f'  Issue: {f["issue"]}')
    print(f'  Code: {f["code"][:80]}')
    print()