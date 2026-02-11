"""Unit tests for quantum computing modules."""
import pytest
import numpy as np


class TestMatrixOps:
    """Test scientific matrix operations as a proxy for quantum linear algebra."""

    def test_eigenvalues(self):
        from src.scientific.analysis.matrix_ops import MatrixOperations
        ops = MatrixOperations()
        H = [[2, -1], [-1, 2]]
        result = ops.execute("eigenvalues", H)
        assert "eigenvalues" in result
        assert len(result["eigenvalues"]) == 2

    def test_svd(self):
        from src.scientific.analysis.matrix_ops import MatrixOperations
        ops = MatrixOperations()
        result = ops.execute("svd", [[1, 2], [3, 4], [5, 6]])
        assert "singular_values" in result
        assert result["rank"] == 2

    def test_solve_linear_system(self):
        from src.scientific.analysis.matrix_ops import MatrixOperations
        ops = MatrixOperations()
        A = [[2, 1], [1, 3]]
        b = [5, 7]
        result = ops.execute("solve", A, vector_b=b)
        assert "solution" in result
        assert result["residual"] < 1e-10

    def test_determinant(self):
        from src.scientific.analysis.matrix_ops import MatrixOperations
        ops = MatrixOperations()
        result = ops.execute("determinant", [[1, 0], [0, 1]])
        assert abs(result["result"] - 1.0) < 1e-10

    def test_inverse(self):
        from src.scientific.analysis.matrix_ops import MatrixOperations
        ops = MatrixOperations()
        result = ops.execute("inverse", [[1, 2], [3, 4]])
        assert "result" in result
        assert "determinant" in result


class TestYAMLConverter:
    def test_yaml_to_json(self):
        from tools.yaml2json import convert_yaml_to_json, validate_yaml
        yaml_str = "name: test\nversion: 1\nitems:\n  - a\n  - b"
        result = convert_yaml_to_json(yaml_str)
        import json
        parsed = json.loads(result)
        assert parsed["name"] == "test"
        assert parsed["version"] == 1
        assert parsed["items"] == ["a", "b"]

    def test_validate_valid_yaml(self):
        from tools.yaml2json import validate_yaml
        result = validate_yaml("key: value")
        assert result["valid"] is True

    def test_validate_invalid_yaml(self):
        from tools.yaml2json import validate_yaml
        result = validate_yaml("key: [invalid\n  yaml:")
        assert result["valid"] is False


class TestStatistics:
    def test_describe(self):
        from src.scientific.analysis.statistics import StatisticalAnalyzer
        analyzer = StatisticalAnalyzer()
        data = [[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]]
        result = analyzer.analyze(data, columns=["a", "b"], operations=["describe"])
        assert "describe" in result
        assert "a" in result["describe"]

    def test_correlation(self):
        from src.scientific.analysis.statistics import StatisticalAnalyzer
        analyzer = StatisticalAnalyzer()
        data = [[1, 2], [2, 4], [3, 6], [4, 8]]
        result = analyzer.analyze(data, columns=["x", "y"], operations=["correlation"])
        assert "correlation" in result
        assert abs(result["correlation"]["x"]["y"] - 1.0) < 1e-6


class TestInterpolation:
    def test_linear_interpolation(self):
        from src.scientific.analysis.interpolation import Interpolator
        interp = Interpolator()
        result = interp.interpolate(x_data=[0, 1, 2, 3], y_data=[0, 1, 4, 9], x_new=[0.5, 1.5, 2.5], method="linear")
        assert "y_interpolated" in result
        assert len(result["y_interpolated"]) == 3


class TestCalculus:
    def test_integration_quad(self):
        from src.scientific.analysis.calculus import NumericalCalculus
        calc = NumericalCalculus()
        result = calc.integrate("x**2", 0, 1, "quad")
        assert abs(result["result"] - 1/3) < 1e-8

    def test_integration_sin(self):
        from src.scientific.analysis.calculus import NumericalCalculus
        calc = NumericalCalculus()
        result = calc.integrate("sin(x)", 0, 3.141592653589793, "quad")
        assert abs(result["result"] - 2.0) < 1e-6


class TestSignalProcessing:
    def test_fft(self):
        from src.scientific.analysis.signal_processing import SignalProcessor
        proc = SignalProcessor()
        signal = [np.sin(2 * np.pi * 5 * t / 100) for t in range(100)]
        result = proc.fft(signal=signal, sample_rate=100)
        assert "dominant_frequency" in result
        assert abs(result["dominant_frequency"] - 5.0) < 1.0