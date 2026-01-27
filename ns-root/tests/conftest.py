"""
GL Governance Markers
@gl-layer GL-80-TEST
@gl-module ns-root/tests
@gl-semantic-anchor GL-80-TESTS_CONFTEST
@gl-evidence-required false
GL Unified Charter Activated
"""

import asyncio
import inspect
import sys
from pathlib import Path

import pytest

# Ensure local packages are importable when tests are invoked from
# repository root
PROJECT_ROOT = Path(__file__).resolve().parents[1]
for candidate in Path(__file__).resolve().parents:
    if (candidate / "namespace_registry").exists() and (
        candidate / "schema_system"
    ).exists():
        PROJECT_ROOT = candidate
        break
root_str = str(PROJECT_ROOT)
if root_str not in sys.path:
    sys.path.insert(0, root_str)


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "asyncio: mark test to run with built-in asyncio event loop support",
    )


@pytest.hookimpl(tryfirst=True)
def pytest_pyfunc_call(pyfuncitem):
    """Minimal async test runner without external plugins."""
    test_obj = pyfuncitem.obj
    if inspect.iscoroutinefunction(test_obj):
        asyncio.run(test_obj(**pyfuncitem.funcargs))
        return True
    return None
