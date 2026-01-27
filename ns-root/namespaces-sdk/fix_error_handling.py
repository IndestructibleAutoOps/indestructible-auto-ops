#!/usr/bin/env python3
"""
GL Governance Markers
@gl-layer GL-00-NAMESPACE
@gl-module ns-root/namespaces-sdk
@gl-semantic-anchor GL-00-NAMESPAC_FIXERRORHAND
@gl-evidence-required false
GL Unified Charter Activated
"""

"""
Fix TypeScript 'error is of type unknown' errors by adding proper type assertions.
"""

import re  # noqa: E402

def fix_error_handling(content: str) -> str:
    """Fix error handling in TypeScript code."""
    
    # Pattern to match catch blocks with error: unknown
    pattern = r'} catch \(error: unknown\) \{([^}]+(?:\{[^}]*\}[^}]*)*)\}'
    
    def replace_catch_block(match):
        body = match.group(1)
        
        # Check if it already has error instanceof check
        if 'error instanceof Error' in body or 'error instanceof SDKError' in body:
            return match.group(0)
        
        # Check if it uses error.message
        if 'error.message' in body or 'error.stack' in body or 'error.code' in body:
            # Add type guard
            new_body = re.sub(r'console\.error\(.*?error\.message', 'if (error instanceof Error) {\n          ' + body.strip().replace('\n', '\n          ') + '\n        } else {\n          console.error(String(error));', body)
            return f'}} catch (error: unknown) {{\n      {new_body}\n    }}'
        
        return match.group(0)
    
    return re.sub(pattern, replace_catch_block, content, flags=re.DOTALL)

def main():
    """
    Deprecated entry point.

    This script previously rewrote TypeScript files to add error-handling
    type guards. Those fixes are expected to already be integrated into the
    source tree, so this script no longer performs any modifications.
    It is kept only to avoid breaking existing tooling that may still invoke it.
    """
    print(
        "fix_error_handling.py is deprecated and no longer modifies any files. "
        "If you need to adjust TypeScript error handling, please do so manually."
    )
    return
if __name__ == '__main__':
    main()