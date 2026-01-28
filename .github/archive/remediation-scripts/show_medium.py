#!/usr/bin/env python3
import json

with open('security_audit_week2.json') as f:
    data = json.load(f)

medium = [f for f in data['findings'] if f['severity'] == 'medium']
print(f'MEDIUM issues: {len(medium)}\n')

for f in medium:
    print(f'{f["file"]}:{f["line"]}')
    print(f'  Category: {f["category"]}')
    print(f'  Issue: {f["issue"]}')
    print()