#!/usr/bin/env python3

"""
GL Semantic Context Manager
===========================
Manages semantic context passing through governance pipeline.

Features:
- Semantic context structure definition
- Context propagation through validation chain
- Context merging and updating
- Context tracking and logging
"""

"""
Module docstring
================

This module is part of the GL governance framework.
Please add specific module documentation here.
"""
# MNGA-002: Import organization needs review
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
import copy


@dataclass
class SemanticContext:
    """
    Semantic context structure.

    Attributes:
        layer: GL semantic layer (e.g., "GL90-99")
        domain: Semantic domain (e.g., "verification")
        context_type: Context type (e.g., "governance", "reporting", "enforcement")
        source: Source of this context (e.g., contract name, operation type)
        timestamp: ISO 8601 timestamp
        metadata: Additional context metadata
        provenance: Provenance chain showing context history
        attributes: Context-specific attributes
    """

    layer: str
    domain: str
    context_type: str
    source: str
    timestamp: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    provenance: List[str] = field(default_factory=list)
    attributes: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert context to dictionary."""
        return {
            "layer": self.layer,
            "domain": self.domain,
            "context_type": self.context_type,
            "source": self.source,
            "timestamp": self.timestamp,
            "metadata": self.metadata,
            "provenance": self.provenance,
            "attributes": self.attributes,
        }

    def to_json(self) -> str:
        """Convert context to JSON string."""
        return json.dumps(self.to_dict(), indent=2)

    def add_provenance(self, step: str):
        """
        Add step to provenance chain.

        Args:
            step: Step description
        """
        self.provenance.append(f"{datetime.utcnow().isoformat()}: {step}")

    def merge(
        self, other: "SemanticContext", strategy: str = "override"
    ) -> "SemanticContext":
        """
        Merge another context into this one.

        Args:
            other: Context to merge
            strategy: Merge strategy ("override", "combine", "prefer_new")

        Returns:
            Merged context
        """
        merged = copy.deepcopy(self)

        if strategy == "override":
            # Override with other context values
            if other.layer:
                merged.layer = other.layer
            if other.domain:
                merged.domain = other.domain
            if other.context_type:
                merged.context_type = other.context_type
            merged.metadata.update(other.metadata)
            merged.attributes.update(other.attributes)

        elif strategy == "combine":
            # Combine values from both contexts
            merged.metadata = {**self.metadata, **other.metadata}
            merged.attributes = {**self.attributes, **other.attributes}
            # Keep other's context_type if more specific
            if other.context_type and other.context_type != self.context_type:
                merged.context_type = f"{self.context_type}+{other.context_type}"

        elif strategy == "prefer_new":
            # Prefer new context but keep existing if not provided
            if other.layer:
                merged.layer = other.layer
            if other.domain:
                merged.domain = other.domain
            if other.context_type:
                merged.context_type = other.context_type
            merged.metadata = {**other.metadata, **self.metadata}
            merged.attributes = {**other.attributes, **self.attributes}

        # Merge provenance
        merged.provenance.extend(other.provenance)

        # Update source and timestamp
        merged.source = f"{self.source} -> {other.source}"
        merged.timestamp = datetime.utcnow().isoformat()

        return merged


class SemanticContextManager:
    """
    Manages semantic context through governance pipeline.

    Handles context extraction, propagation, merging, and tracking.
    """

    def __init__(self, base_path: str = None):
        """
        Initialize semantic context manager.

        Args:
            base_path: Base path for governance operations
        """
        if base_path is None:
            base_path = self._detect_base_path()
        self.base_path = Path(base_path)
        self.current_context: Optional[SemanticContext] = None
        self.context_history: List[SemanticContext] = []
        self.context_log_file = (
            self.base_path / "ecosystem" / "logs" / "semantic_context.log"
        )
        self.context_log_file.parent.mkdir(parents=True, exist_ok=True)

    def _detect_base_path(self) -> str:
        """Auto-detect project base path by looking for governance-manifest.yaml"""
        current = Path(__file__).parent  # ecosystem/semantic
        while current != current.parent:
            if (current / "governance-manifest.yaml").exists():
                return str(current)
            if (current / "ecosystem").exists() and (
                current / "ecosystem" / "enforce.py"
            ).exists():
                return str(current)
            current = current.parent
        # Fallback to parent of ecosystem directory
        return str(Path(__file__).parent.parent.parent)

    def extract_context_from_contract(
        self, contract: Dict
    ) -> Optional[SemanticContext]:
        """
        Extract semantic context from contract metadata.

        Args:
            contract: Contract dictionary

        Returns:
            SemanticContext or None
        """
        metadata = contract.get("metadata", {})

        if not metadata:
            return None

        context = SemanticContext(
            layer=metadata.get("gl_semantic_layer", ""),
            domain=metadata.get("gl_semantic_domain", ""),
            context_type=metadata.get("gl_semantic_context", ""),
            source=contract.get("component_type", "contract"),
            timestamp=datetime.utcnow().isoformat(),
            metadata={
                "contract_version": contract.get("version", ""),
                "contract_status": contract.get("status", ""),
            },
        )

        context.add_provenance(f"Extracted from contract")

        return context

    def extract_context_from_operation(
        self, operation: Dict
    ) -> Optional[SemanticContext]:
        """
        Extract semantic context from operation.

        Args:
            operation: Operation dictionary

        Returns:
            SemanticContext or None
        """
        operation_type = operation.get("type", "unknown")

        context = SemanticContext(
            layer="GL90-99",
            domain="operations",
            context_type=operation_type,
            source=f"operation:{operation_type}",
            timestamp=datetime.utcnow().isoformat(),
            metadata={
                "files": operation.get("files", []),
                "operation_type": operation_type,
            },
        )

        context.add_provenance(f"Extracted from operation")

        return context

    def set_context(self, context: SemanticContext):
        """
        Set current semantic context.

        Args:
            context: Context to set
        """
        if self.current_context:
            self.context_history.append(self.current_context)

        self.current_context = context
        self._log_context(context, "SET")

    def get_context(self) -> Optional[SemanticContext]:
        """
        Get current semantic context.

        Returns:
            Current context or None
        """
        return self.current_context

    def update_context(self, **kwargs):
        """
        Update current semantic context.

        Args:
            **kwargs: Context attributes to update
        """
        if not self.current_context:
            return

        for key, value in kwargs.items():
            if hasattr(self.current_context, key):
                setattr(self.current_context, key, value)
            elif key in self.current_context.metadata:
                self.current_context.metadata[key] = value
            else:
                self.current_context.metadata[key] = value

        self.current_context.add_provenance(
            f"Updated context: {', '.join(kwargs.keys())}"
        )
        self._log_context(self.current_context, "UPDATE")

    def merge_context(self, other: SemanticContext, strategy: str = "override"):
        """
        Merge another context into current context.

        Args:
            other: Context to merge
            strategy: Merge strategy
        """
        if not self.current_context:
            self.set_context(other)
        else:
            self.current_context = self.current_context.merge(other, strategy)
            self.current_context.add_provenance(
                f"Merged with context from {other.source}"
            )
            self._log_context(self.current_context, "MERGE")

    def clear_context(self):
        """Clear current semantic context."""
        if self.current_context:
            self.context_history.append(self.current_context)
            self._log_context(self.current_context, "CLEAR")

        self.current_context = None

    def get_context_history(self, limit: int = 10) -> List[SemanticContext]:
        """
        Get recent context history.

        Args:
            limit: Maximum number of contexts to return

        Returns:
            List of recent contexts
        """
        return self.context_history[-limit:]

    def propagate_context(self, operation: Dict) -> Dict:
        """
        Propagate current context to operation.

        Args:
            operation: Operation to add context to

        Returns:
            Operation with context added
        """
        if not self.current_context:
            return operation

        operation_with_context = copy.deepcopy(operation)
        operation_with_context["semantic_context"] = self.current_context.to_dict()

        return operation_with_context

    def track_context_flow(self, stage: str, context: SemanticContext):
        """
        Track context flow through pipeline stage.

        Args:
            stage: Pipeline stage name
            context: Context at this stage
        """
        context.add_provenance(f"Pipeline stage: {stage}")
        self._log_context(context, f"STAGE:{stage}")

    def _log_context(self, context: SemanticContext, action: str):
        """
        Log context change.

        Args:
            context: Context being logged
            action: Action being performed
        """
        timestamp = datetime.utcnow().isoformat()
        log_entry = f"[{timestamp}] {action} - {context.to_json()}\n"

        with open(self.context_log_file, "a") as f:
            f.write(log_entry)

    def validate_context(self, context: SemanticContext) -> bool:
        """
        Validate semantic context.

        Args:
            context: Context to validate

        Returns:
            True if valid
        """
        # Check required fields
        if not context.layer or not context.domain or not context.context_type:
            return False

        # Check layer format
        if not context.layer.startswith("GL"):
            return False

        # Check timestamp format
        try:
            datetime.fromisoformat(context.timestamp)
        except ValueError:
            return False

        return True

    def get_context_summary(self) -> Dict[str, Any]:
        """
        Get summary of current context and history.

        Returns:
            Context summary dictionary
        """
        summary = {
            "current_context": None,
            "history_length": len(self.context_history),
            "validation_status": "no_context",
        }

        if self.current_context:
            summary["current_context"] = {
                "layer": self.current_context.layer,
                "domain": self.current_context.domain,
                "context_type": self.current_context.context_type,
                "source": self.current_context.source,
                "timestamp": self.current_context.timestamp,
                "provenance_length": len(self.current_context.provenance),
            }
            summary["validation_status"] = (
                "valid" if self.validate_context(self.current_context) else "invalid"
            )

        return summary


# Global context manager instance
_global_context_manager = None


def get_global_context_manager(base_path: str = None) -> SemanticContextManager:
    """
    Get global semantic context manager instance.

    Args:
        base_path: Base path for governance operations

    Returns:
        Global SemanticContextManager instance
    """
    global _global_context_manager

    if _global_context_manager is None:
        _global_context_manager = SemanticContextManager(base_path)

    return _global_context_manager
