# @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: archive-tools
# @GL-audit-trail: ../../engine/gl_platform_universe.gl_platform_universe.governance/GL_SEMANTIC_ANCHOR.json
#
# GL Unified Charter Activated
#!/usr/bin/env python3
"""
Module docstring
================

This module is part of the GL governance framework.
Please add specific module documentation here.
"""
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