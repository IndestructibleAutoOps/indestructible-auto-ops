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

with open('security_audit_post_fix.json') as f:
    data = json.load(f)

critical = [f for f in data['findings'] if f['severity'] == 'critical']
print(f'Remaining CRITICAL findings: {len(critical)}\n')

for f in critical:
    print(f'{f["file"]}:{f["line"]}')
    print(f'  Issue: {f["issue"]}')
    print(f'  Code: {f["code"][:80]}')
    print()