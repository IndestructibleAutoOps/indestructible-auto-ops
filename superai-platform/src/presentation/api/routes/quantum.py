"""Quantum Computing API routes - Qiskit Runtime, VQE, QAOA, QML."""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Query
from pydantic import BaseModel, Field

router = APIRouter()


# --- Schemas ---
class CircuitRequest(BaseModel):
    num_qubits: int = Field(..., ge=1, le=30, description="Number of qubits")
    circuit_type: str = Field(default="bell", pattern=r"^(bell|ghz|qft|grover|custom)$")
    shots: int = Field(default=1024, ge=1, le=100000)
    parameters: dict[str, Any] = Field(default_factory=dict)


class VQERequest(BaseModel):
    hamiltonian: list[list[float]] = Field(..., description="Hamiltonian matrix")
    num_qubits: int = Field(..., ge=1, le=20)
    ansatz: str = Field(default="ry", pattern=r"^(ry|ryrz|efficient_su2|hardware_efficient)$")
    optimizer: str = Field(default="cobyla", pattern=r"^(cobyla|spsa|adam|l_bfgs_b)$")
    max_iterations: int = Field(default=100, ge=1, le=10000)
    shots: int = Field(default=1024, ge=1, le=100000)


class QAOARequest(BaseModel):
    cost_matrix: list[list[float]] = Field(..., description="Cost matrix for optimization")
    num_layers: int = Field(default=2, ge=1, le=20)
    optimizer: str = Field(default="cobyla", pattern=r"^(cobyla|spsa|adam)$")
    shots: int = Field(default=1024, ge=1, le=100000)


class QMLRequest(BaseModel):
    training_data: list[list[float]] = Field(..., description="Training feature vectors")
    training_labels: list[int] = Field(..., description="Training labels")
    test_data: list[list[float]] = Field(default_factory=list)
    feature_map: str = Field(default="zz", pattern=r"^(zz|pauli|amplitude)$")
    ansatz: str = Field(default="real_amplitudes")
    epochs: int = Field(default=50, ge=1, le=1000)


class QuantumResult(BaseModel):
    job_id: str
    status: str
    result: dict[str, Any] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)
    execution_time_ms: float = 0.0


class YAMLConvertRequest(BaseModel):
    yaml_content: str = Field(..., description="YAML string to convert")


# --- Endpoints ---
@router.post("/circuits/execute", response_model=QuantumResult)
async def execute_circuit(request: CircuitRequest) -> dict[str, Any]:
    """Execute a quantum circuit on the configured backend."""
    from src.quantum.runtime.executor import QuantumExecutor
    executor = QuantumExecutor()
    return await executor.run_circuit(
        num_qubits=request.num_qubits,
        circuit_type=request.circuit_type,
        shots=request.shots,
        parameters=request.parameters,
    )


@router.post("/vqe/solve", response_model=QuantumResult)
async def solve_vqe(request: VQERequest) -> dict[str, Any]:
    """Solve a variational quantum eigensolver problem."""
    from src.quantum.algorithms.vqe import VQESolver
    solver = VQESolver()
    return await solver.solve(
        hamiltonian=request.hamiltonian,
        num_qubits=request.num_qubits,
        ansatz=request.ansatz,
        optimizer=request.optimizer,
        max_iterations=request.max_iterations,
        shots=request.shots,
    )


@router.post("/qaoa/optimize", response_model=QuantumResult)
async def optimize_qaoa(request: QAOARequest) -> dict[str, Any]:
    """Run QAOA combinatorial optimization."""
    from src.quantum.algorithms.qaoa import QAOASolver
    solver = QAOASolver()
    return await solver.optimize(
        cost_matrix=request.cost_matrix,
        num_layers=request.num_layers,
        optimizer=request.optimizer,
        shots=request.shots,
    )


@router.post("/qml/classify", response_model=QuantumResult)
async def qml_classify(request: QMLRequest) -> dict[str, Any]:
    """Train and run a quantum machine learning classifier."""
    from src.quantum.algorithms.qml import QMLClassifier
    classifier = QMLClassifier()
    return await classifier.train_and_predict(
        training_data=request.training_data,
        training_labels=request.training_labels,
        test_data=request.test_data,
        feature_map=request.feature_map,
        ansatz=request.ansatz,
        epochs=request.epochs,
    )


@router.get("/backends", response_model=list[dict[str, Any]])
async def list_backends() -> list[dict[str, Any]]:
    """List available quantum backends."""
    from src.quantum.runtime.executor import QuantumExecutor
    executor = QuantumExecutor()
    return executor.list_backends()


@router.post("/tools/yaml-to-json")
async def yaml_to_json(request: YAMLConvertRequest) -> dict[str, Any]:
    """Convert YAML to JSON format."""
    import yaml
    import json
    try:
        parsed = yaml.safe_load(request.yaml_content)
        return {"status": "success", "json": parsed, "json_string": json.dumps(parsed, indent=2, ensure_ascii=False)}
    except yaml.YAMLError as e:
        return {"status": "error", "message": f"Invalid YAML: {e}"}