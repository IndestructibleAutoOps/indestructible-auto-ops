#!/usr/bin/env python3
"""
GL Governance Markers
@gl-layer GL-00-NAMESPACE
@gl-module ns-root/namespaces-sdk
@gl-semantic-anchor GL-00-NAMESPAC_FIXGITHUBTOO
@gl-evidence-required false
GL Unified Charter Activated
"""

"""Deprecated wrapper for GitHub tools fix script.

This module previously contained an alternative implementation of the GitHub
tools fix logic, which led to multiple competing versions of the same script
(for example: fix_github_tools.py, fix_github_tools_v2.py, fix_tools_final.py).

To avoid confusion and to comply with the single source principle, this file
is now deprecated and no longer performs any modifications. Use the canonical
fix script or the in-source fixes instead.
"""

import warnings  # noqa: E402


def fix_github_tools() -> None:
    """Deprecated: use the canonical GitHub tools fix script instead.

    This function is intentionally unimplemented to prevent this file from
    acting as a competing version of the GitHub tools fix script.
    """
    warnings.warn(
        "fix_github_tools_v2.py is deprecated. "
        "Use the canonical GitHub tools fix script or rely on in-source fixes.",
        DeprecationWarning,
        stacklevel=2,
    )
    return