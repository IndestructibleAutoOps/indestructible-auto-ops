"""Unit tests for API schemas validation."""
from __future__ import annotations

import pytest
from pydantic import ValidationError

from src.presentation.api.schemas import (
    UserCreateRequest,
    UserUpdateRequest,
    LoginRequest,
    CircuitRequest,
    VQERequest,
    ExpertCreateRequest,
    MatrixRequest,
    OptimizationRequest,
)


class TestUserSchemas:
    def test_valid_user_create(self):
        req = UserCreateRequest(
            username="john_doe",
            email="john@example.com",
            password="SecureP@ss1",
            full_name="John Doe",
            role="developer",
        )
        assert req.username == "john_doe"

    def test_username_too_short(self):
        with pytest.raises(ValidationError):
            UserCreateRequest(username="ab", email="a@b.com", password="SecureP@ss1")

    def test_username_invalid_chars(self):
        with pytest.raises(ValidationError):
            UserCreateRequest(username="bad user!", email="a@b.com", password="SecureP@ss1")

    def test_invalid_role(self):
        with pytest.raises(ValidationError):
            UserCreateRequest(username="test", email="a@b.com", password="SecureP@ss1", role="superadmin")

    def test_password_too_short(self):
        with pytest.raises(ValidationError):
            UserCreateRequest(username="test", email="a@b.com", password="short")

    def test_user_update_partial(self):
        req = UserUpdateRequest(full_name="New Name")
        assert req.full_name == "New Name"
        assert req.role is None

    def test_login_request(self):
        req = LoginRequest(username="test", password="pass")
        assert req.username == "test"


class TestQuantumSchemas:
    def test_valid_circuit_request(self):
        req = CircuitRequest(num_qubits=4, circuit_type="ghz", shots=500)
        assert req.num_qubits == 4

    def test_qubits_out_of_range(self):
        with pytest.raises(ValidationError):
            CircuitRequest(num_qubits=0)
        with pytest.raises(ValidationError):
            CircuitRequest(num_qubits=31)

    def test_invalid_circuit_type(self):
        with pytest.raises(ValidationError):
            CircuitRequest(num_qubits=2, circuit_type="invalid")

    def test_shots_range(self):
        with pytest.raises(ValidationError):
            CircuitRequest(num_qubits=2, shots=0)
        with pytest.raises(ValidationError):
            CircuitRequest(num_qubits=2, shots=200000)

    def test_vqe_request(self):
        req = VQERequest(
            hamiltonian=[[1.0, 0.0], [0.0, -1.0]],
            num_qubits=2,
            ansatz="ry",
            optimizer="cobyla",
        )
        assert req.num_qubits == 2


class TestAISchemas:
    def test_expert_create(self):
        req = ExpertCreateRequest(name="Quantum Expert", domain="quantum")
        assert req.name == "Quantum Expert"
        assert req.temperature == 0.7

    def test_temperature_range(self):
        with pytest.raises(ValidationError):
            ExpertCreateRequest(name="test", domain="test", temperature=3.0)


class TestScientificSchemas:
    def test_matrix_request(self):
        req = MatrixRequest(matrix=[[1.0, 2.0], [3.0, 4.0]])
        assert len(req.matrix) == 2

    def test_optimization_request(self):
        req = OptimizationRequest(
            method="minimize",
            objective="x[0]**2 + x[1]**2",
            initial_guess=[1.0, 1.0],
        )
        assert req.method == "minimize"