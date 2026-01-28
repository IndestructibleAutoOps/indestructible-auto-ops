/**
 * @GL-governed
 * @GL-layer: governance
 * @GL-semantic: validate_pr1063_layers
 * @GL-audit-trail: ../../engine/governance/GL_SEMANTIC_ANCHOR.json
 *
 * GL Unified Charter Activated
 */

#!/usr/bin/env python3
"""
Shim to reuse PR #1023 layer validator for PR #1063 context.
"""
from tools.validation.validate_pr1023_layers import main

if __name__ == "__main__":
    raise SystemExit(main())
