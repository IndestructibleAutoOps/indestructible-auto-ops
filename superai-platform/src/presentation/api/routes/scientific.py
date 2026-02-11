"""Scientific Computing API routes - NumPy, Pandas, SciPy, Scikit-learn."""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, UploadFile, File, Query
from pydantic import BaseModel, Field

router = APIRouter()


# --- Schemas ---
class MatrixOperationRequest(BaseModel):
    operation: str = Field(..., pattern=r"^(multiply|inverse|eigenvalues|svd|determinant|transpose|norm|solve)$")
    matrix_a: list[list[float]] = Field(..., description="Primary matrix")
    matrix_b: list[list[float]] | None = Field(None, description="Secondary matrix (for multiply/solve)")
    vector_b: list[float] | None = Field(None, description="Vector b (for solve Ax=b)")


class StatisticsRequest(BaseModel):
    data: list[list[float]] = Field(..., description="Data matrix (rows=samples, cols=features)")
    columns: list[str] = Field(default_factory=list)
    operations: list[str] = Field(
        default=["describe"],
        description="Operations: describe, correlation, covariance, histogram, outliers"
    )


class OptimizationRequest(BaseModel):
    method: str = Field(default="minimize", pattern=r"^(minimize|curve_fit|root|linprog|milp)$")
    objective: str = Field(..., description="Objective function as string expression")
    bounds: list[list[float]] = Field(default_factory=list)
    constraints: list[dict[str, Any]] = Field(default_factory=list)
    initial_guess: list[float] = Field(default_factory=list)
    parameters: dict[str, Any] = Field(default_factory=dict)


class MLTrainRequest(BaseModel):
    algorithm: str = Field(..., pattern=r"^(linear_regression|logistic_regression|random_forest|svm|kmeans|pca|gradient_boosting|decision_tree|knn)$")
    features: list[list[float]] = Field(..., description="Feature matrix")
    labels: list[float] | list[int] | None = Field(None, description="Labels (None for unsupervised)")
    test_size: float = Field(default=0.2, ge=0.05, le=0.5)
    hyperparameters: dict[str, Any] = Field(default_factory=dict)
    cross_validation: int = Field(default=0, ge=0, le=20, description="K-fold CV (0=disabled)")


class MLPredictRequest(BaseModel):
    model_id: str = Field(..., description="Trained model identifier")
    features: list[list[float]] = Field(..., description="Feature matrix for prediction")


class InterpolationRequest(BaseModel):
    x_data: list[float] = Field(..., description="Known x values")
    y_data: list[float] = Field(..., description="Known y values")
    x_new: list[float] = Field(..., description="New x values to interpolate")
    method: str = Field(default="cubic", pattern=r"^(linear|cubic|quadratic|nearest|pchip)$")


class FFTRequest(BaseModel):
    signal: list[float] = Field(..., description="Input signal")
    sample_rate: float = Field(default=1.0, gt=0)
    inverse: bool = False


class IntegrationRequest(BaseModel):
    function: str = Field(..., description="Function expression (variable: x)")
    lower_bound: float
    upper_bound: float
    method: str = Field(default="quad", pattern=r"^(quad|trapezoid|simpson|romberg)$")


# --- Endpoints ---
@router.post("/matrix")
async def matrix_operation(request: MatrixOperationRequest) -> dict[str, Any]:
    """Perform matrix operations using NumPy."""
    from src.scientific.analysis.matrix_ops import MatrixOperations
    ops = MatrixOperations()
    return ops.execute(
        operation=request.operation,
        matrix_a=request.matrix_a,
        matrix_b=request.matrix_b,
        vector_b=request.vector_b,
    )


@router.post("/statistics")
async def compute_statistics(request: StatisticsRequest) -> dict[str, Any]:
    """Compute statistical analysis using Pandas and SciPy."""
    from src.scientific.analysis.statistics import StatisticalAnalyzer
    analyzer = StatisticalAnalyzer()
    return analyzer.analyze(
        data=request.data,
        columns=request.columns,
        operations=request.operations,
    )


@router.post("/optimize")
async def optimize(request: OptimizationRequest) -> dict[str, Any]:
    """Run optimization using SciPy."""
    from src.scientific.analysis.optimizer import ScientificOptimizer
    optimizer = ScientificOptimizer()
    return optimizer.solve(
        method=request.method,
        objective=request.objective,
        bounds=request.bounds,
        constraints=request.constraints,
        initial_guess=request.initial_guess,
        parameters=request.parameters,
    )


@router.post("/ml/train")
async def train_model(request: MLTrainRequest) -> dict[str, Any]:
    """Train a machine learning model using Scikit-learn."""
    from src.scientific.ml.trainer import MLTrainer
    trainer = MLTrainer()
    return await trainer.train(
        algorithm=request.algorithm,
        features=request.features,
        labels=request.labels,
        test_size=request.test_size,
        hyperparameters=request.hyperparameters,
        cross_validation=request.cross_validation,
    )


@router.post("/ml/predict")
async def predict(request: MLPredictRequest) -> dict[str, Any]:
    """Run predictions using a trained model."""
    from src.scientific.ml.trainer import MLTrainer
    trainer = MLTrainer()
    return await trainer.predict(model_id=request.model_id, features=request.features)


@router.get("/ml/models")
async def list_models() -> list[dict[str, Any]]:
    """List all trained models."""
    from src.scientific.ml.trainer import MLTrainer
    trainer = MLTrainer()
    return await trainer.list_models()


@router.post("/interpolation")
async def interpolate(request: InterpolationRequest) -> dict[str, Any]:
    """Perform data interpolation using SciPy."""
    from src.scientific.analysis.interpolation import Interpolator
    interp = Interpolator()
    return interp.interpolate(
        x_data=request.x_data,
        y_data=request.y_data,
        x_new=request.x_new,
        method=request.method,
    )


@router.post("/fft")
async def fft_analysis(request: FFTRequest) -> dict[str, Any]:
    """Perform FFT/IFFT analysis."""
    from src.scientific.analysis.signal_processing import SignalProcessor
    processor = SignalProcessor()
    return processor.fft(signal=request.signal, sample_rate=request.sample_rate, inverse=request.inverse)


@router.post("/integrate")
async def integrate(request: IntegrationRequest) -> dict[str, Any]:
    """Numerical integration using SciPy."""
    from src.scientific.analysis.calculus import NumericalCalculus
    calc = NumericalCalculus()
    return calc.integrate(
        function=request.function,
        lower_bound=request.lower_bound,
        upper_bound=request.upper_bound,
        method=request.method,
    )