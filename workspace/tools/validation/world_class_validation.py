"""
World-class validation manifest loader (concept draft).

Aligns with:
- YAML manifest: workspace/config/validation/world-class-validation.yaml
- JSON Schema:   workspace/config/validation/schemas/world-class-validation.schema.json
- TS types:      workspace/config/validation/worldClassValidation.ts
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import yaml

MANIFEST_PATH = Path("workspace/config/validation/world-class-validation.yaml")
SCHEMA_PATH = Path(
    "workspace/config/validation/schemas/world-class-validation.schema.json"
)


@dataclass
class EnhancedValidationDimension:
    dimension: str
    accuracy: float | None = None
    techniques: list[str] | None = None
    dimensions: int | None = None
    coverage: float | None = None
    standards: list[str] | None = None
    technologies: list[str] | None = None
    prediction_accuracy: float | None = None
    horizon: str | None = None


@dataclass
class PerformanceTargets:
    validationSpeed: str
    falsePositiveRate: float
    falseNegativeRate: float
    coverage: float


@dataclass
class ImplementationRequirements:
    quantumHardware: str
    aiAcceleration: str
    blockchainIntegration: str
    realTimeMonitoring: str
    automatedRemediation: str


@dataclass
class WorldClassValidationSpec:
    enhancedValidationDimensions: list[EnhancedValidationDimension]
    performanceTargets: PerformanceTargets
    implementationRequirements: ImplementationRequirements


@dataclass
class WorldClassValidationManifest:
    apiVersion: str
    kind: str
    metadata: dict
    spec: WorldClassValidationSpec


def load_manifest(path: Path = MANIFEST_PATH) -> WorldClassValidationManifest:
    """Load YAML manifest into typed dataclasses (no schema validation here)."""
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    spec = data["spec"]
    dims = [
        EnhancedValidationDimension(**item)
        for item in spec.get("enhancedValidationDimensions", [])
    ]
    perf = PerformanceTargets(**spec["performanceTargets"])
    impl = ImplementationRequirements(**spec["implementationRequirements"])
    spec_obj = WorldClassValidationSpec(
        enhancedValidationDimensions=dims,
        performanceTargets=perf,
        implementationRequirements=impl,
    )
    return WorldClassValidationManifest(
        apiVersion=data["apiVersion"],
        kind=data["kind"],
        metadata=data["metadata"],
        spec=spec_obj,
    )


def load_schema(path: Path = SCHEMA_PATH) -> dict:
    """Load JSON Schema for optional validation tooling."""
    return json.loads(path.read_text(encoding="utf-8"))


__all__ = [
    "load_manifest",
    "load_schema",
    "WorldClassValidationManifest",
    "WorldClassValidationSpec",
    "EnhancedValidationDimension",
    "PerformanceTargets",
    "ImplementationRequirements",
]
