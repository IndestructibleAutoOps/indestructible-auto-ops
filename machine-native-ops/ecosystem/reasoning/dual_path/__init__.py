"""
GL Dual-Path Retrieval + Arbitration System
MNGA Layer 6 (Reasoning)

@GL-semantic: dual-path-retrieval-system
@GL-audit-trail: enabled
"""

from .internal.retrieval import InternalRetrievalEngine
from .external.retrieval import ExternalRetrievalEngine
from .arbitration import Arbitrator
from ..traceability.traceability import TraceabilityEngine
from .pipeline import ReasoningPipeline

__version__ = "1.0.0"
__all__ = [
    "InternalRetrievalEngine",
    "ExternalRetrievalEngine",
    "Arbitrator",
    "TraceabilityEngine",
    "ReasoningPipeline",
]
