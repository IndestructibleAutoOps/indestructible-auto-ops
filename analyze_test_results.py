#!/usr/bin/env python3
import json

with open('phase4_integration_test_results_20260209_215709.json', 'r') as f:
    data = json.load(f)

legacy_issues = [issue for issue in data['summary']['issues_found'] if 'legacy' in issue['type']]

print('LEGACY gl- REFERENCES FOUND:')
print('='*80)
for issue in legacy_issues[:20]:
    print(f"File: {issue['file']}")
    print(f"Type: {issue['type']}")
    print(f"Details: {issue['details']}")
    print('-'*80)

print(f'\nTotal legacy gl- issues: {len(legacy_issues)}')
print(f'  - legacy_gl_reference: {len([i for i in legacy_issues if i["type"] == "legacy_gl_reference"])}')
print(f'  - legacy_gl_link: {len([i for i in legacy_issues if i["type"] == "legacy_gl_link"])}')
print(f'  - legacy_gl_path: {len([i for i in legacy_issues if i["type"] == "legacy_gl_path"])}')