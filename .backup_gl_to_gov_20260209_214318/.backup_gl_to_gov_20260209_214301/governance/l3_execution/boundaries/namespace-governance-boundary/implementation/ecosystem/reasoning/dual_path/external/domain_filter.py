"""Domain filter placeholder for MNGA external reasoning path."""


class DomainFilter:
    """Stub domain filter."""

    def allow(self, domain: str) -> bool:
        return True
"""Compatibility wrapper for the external domain filter."""

try:
    from .._loader import load_impl

    _impl = load_impl(
        "external/domain_filter.py",
        "ecosystem.reasoning.dual_path.external.domain_filter.impl",
    )
    DomainFilter = _impl.DomainFilter
except Exception:  # pragma: no cover - fallback when implementation is missing

    class DomainFilter:
        """Fallback domain filter that blocks nothing."""

        def __init__(self, *args, **kwargs):
            self.unavailable = True

        def is_allowed(self, url: str) -> bool:
            return True


__all__ = ["DomainFilter"]
