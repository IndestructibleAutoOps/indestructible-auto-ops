"""Centralized API request/response schemas — Pydantic models for validation."""
from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


# --- Common ---

class ErrorDetail(BaseModel):
    field: str | None = None
    message: str


class ErrorResponse(BaseModel):
    code: str
    message: str
    details: list[ErrorDetail] = Field(default_factory=list)
    request_id: str | None = None
    timestamp: str | None = None


class PaginationParams(BaseModel):
    skip: int = Field(default=0, ge=0)
    limit: int = Field(default=20, ge=1, le=100)


class PaginatedResponse(BaseModel):
    items: list[Any]
    total: int
    skip: int
    limit: int
    has_next: bool = False


# --- User Schemas ---

class UserCreateRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, pattern=r"^[a-zA-Z0-9_-]+$")
    email: str = Field(..., max_length=254, description="Valid email address")
    password: str = Field(..., min_length=8, max_length=128)
    full_name: str = Field(default="", max_length=200)
    role: str = Field(default="viewer", pattern=r"^(admin|operator|scientist|developer|viewer)$")


class UserUpdateRequest(BaseModel):
    full_name: str | None = Field(None, max_length=200)
    role: str | None = Field(None, pattern=r"^(admin|operator|scientist|developer|viewer)$")


class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    full_name: str
    role: str
    status: str
    created_at: str
    last_login_at: str | None = None
    login_count: int = 0


class UserListResponse(PaginatedResponse):
    items: list[UserResponse]  # type: ignore[assignment]


class LoginRequest(BaseModel):
    username: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class RefreshTokenRequest(BaseModel):
    refresh_token: str


# --- Quantum Schemas ---

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


class QuantumResultResponse(BaseModel):
    job_id: str
    status: str
    result: dict[str, Any] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)
    execution_time_ms: float = 0.0


# --- AI Schemas ---

class ExpertCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    domain: str = Field(..., min_length=1, max_length=50)
    specialization: str = Field(default="", max_length=200)
    knowledge_base: list[str] = Field(default_factory=list)
    model: str = Field(default="gpt-4-turbo-preview")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    system_prompt: str = Field(default="", max_length=5000)


class ExpertQueryRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=10000)
    context: dict[str, Any] = Field(default_factory=dict)
    max_tokens: int = Field(default=2000, ge=1, le=16000)
    include_sources: bool = Field(default=False)


class VectorStoreRequest(BaseModel):
    collection: str = Field(..., min_length=1, max_length=100)
    documents: list[str] = Field(..., min_items=1)
    metadatas: list[dict[str, Any]] = Field(default_factory=list)
    ids: list[str] = Field(default_factory=list)


class VectorSearchRequest(BaseModel):
    collection: str = Field(..., min_length=1, max_length=100)
    query: str = Field(..., min_length=1, max_length=5000)
    top_k: int = Field(default=10, ge=1, le=100)
    threshold: float = Field(default=0.0, ge=0.0, le=1.0)


class EmbeddingRequest(BaseModel):
    texts: list[str] = Field(..., min_items=1, max_items=100)
    model: str = Field(default="text-embedding-3-small")


# --- Scientific Schemas ---

class MatrixRequest(BaseModel):
    matrix: list[list[float]] = Field(..., description="Input matrix")
    compute_vectors: bool = Field(default=True)


class LinearSystemRequest(BaseModel):
    coefficients: list[list[float]] = Field(..., description="Coefficient matrix A")
    constants: list[float] = Field(..., description="Constants vector b")


class StatisticsRequest(BaseModel):
    data: list[float] = Field(..., min_items=1, description="Data array")
    confidence_level: float = Field(default=0.95, ge=0.5, le=0.999)


class OptimizationRequest(BaseModel):
    method: str = Field(default="minimize", pattern=r"^(minimize|root|linprog|curve_fit)$")
    objective: str = Field(..., description="Objective function expression")
    bounds: list[list[float]] = Field(default_factory=list)
    constraints: list[dict[str, Any]] = Field(default_factory=list)
    initial_guess: list[float] = Field(default_factory=list)
    parameters: dict[str, Any] = Field(default_factory=dict)


class MLTrainRequest(BaseModel):
    model_type: str = Field(default="random_forest", pattern=r"^(random_forest|gradient_boosting|svm|neural_network|linear_regression|logistic_regression)$")
    task: str = Field(default="classification", pattern=r"^(classification|regression)$")
    features: list[list[float]] = Field(..., description="Feature matrix")
    labels: list[float] = Field(..., description="Target labels")
    test_size: float = Field(default=0.2, ge=0.05, le=0.5)
    hyperparameters: dict[str, Any] = Field(default_factory=dict)


__all__ = [
    "ErrorResponse", "ErrorDetail", "PaginationParams", "PaginatedResponse",
    "UserCreateRequest", "UserUpdateRequest", "UserResponse", "UserListResponse",
    "LoginRequest", "TokenResponse", "RefreshTokenRequest",
    "CircuitRequest", "VQERequest", "QAOARequest", "QMLRequest", "QuantumResultResponse",
    "ExpertCreateRequest", "ExpertQueryRequest", "VectorStoreRequest", "VectorSearchRequest", "EmbeddingRequest",
    "MatrixRequest", "LinearSystemRequest", "StatisticsRequest", "OptimizationRequest", "MLTrainRequest",
]