# @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: archive-tools
# @GL-audit-trail: ../../engine/gl_platform_universegl_platform_universe.governance/GL_SEMANTIC_ANCHOR.json
#
# GL Unified Charter Activated
#
# @GL-governed
# @GL-layer: gl_platform_universegl_platform_universe.governance
# @GL-semantic: validate_pr1063_layers
# @GL-audit-trail: ../../engine/gl_platform_universegl_platform_universe.governance/GL_SEMANTIC_ANCHOR.json
#
#!/usr/bin/env python3
"""
Shim to reuse PR #1023 layer validator for PR #1063 context.
"""
from tools.validation.validate_pr1023_layers import main
if __name__ == "__main__":
    raise SystemExit(main())
