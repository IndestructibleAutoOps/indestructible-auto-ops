# FILE: tests/unit/test_parametric_convergence.py
# 單元測試：參數化收斂

import pytest
import numpy as np
from typing import Callable, Dict, List
import math


class MockConvergenceMetrics:
    """Mock Convergence Metrics"""
    def __init__(self, iteration: int, parameter_change: float, loss: float,
                 gradient_norm: float, lipschitz_constant: float, is_converged: bool):
        self.iteration = iteration
        self.parameter_change = parameter_change
        self.loss = loss
        self.gradient_norm = gradient_norm
        self.lipschitz_constant = lipschitz_constant
        self.is_converged = is_converged


class MockParametricConvergenceGuarantee:
    """Mock Parametric Convergence Guarantee"""
    
    def __init__(self, parameter_space_bounds: Dict):
        self.bounds = parameter_space_bounds
        self.update_history: List[MockConvergenceMetrics] = []
        self.lipschitz_constant = None
    
    def verify_lipschitz_continuity(self, update_function: Callable, 
                                    sample_size: int = 100) -> float:
        """Verify Lipschitz continuity"""
        samples = self._sample_parameter_space(sample_size)
        
        max_ratio = 0
        for i in range(len(samples) - 1):
            p1, p2 = samples[i], samples[i + 1]
            
            delta_p = np.linalg.norm(p1 - p2)
            delta_f = np.linalg.norm(
                update_function(p1) - update_function(p2)
            )
            
            if delta_p > 1e-6:
                ratio = delta_f / delta_p
                max_ratio = max(max_ratio, ratio)
        
        self.lipschitz_constant = max_ratio
        
        if self.lipschitz_constant >= 1.0:
            raise ValueError(
                f"Lipschitz constant {self.lipschitz_constant} >= 1, "
                "convergence not guaranteed"
            )
        
        return self.lipschitz_constant
    
    def predict_convergence_time(self, initial_error: float, 
                                 target_error: float) -> int:
        """Predict convergence time"""
        if self.lipschitz_constant is None:
            raise ValueError("Lipschitz constant not computed")
        
        n = math.log(target_error / initial_error) / math.log(
            self.lipschitz_constant
        )
        
        return int(np.ceil(n))
    
    def monitor_convergence(self, parameters: np.ndarray, loss: float,
                           gradient: np.ndarray) -> MockConvergenceMetrics:
        """Monitor convergence"""
        if len(self.update_history) > 0:
            prev_params = self.update_history[-1].parameter_change
            param_change = np.linalg.norm(parameters - prev_params)
        else:
            param_change = np.inf
        
        gradient_norm = np.linalg.norm(gradient)
        
        is_converged = (
            param_change < 1e-4 and
            gradient_norm < 1e-3
        )
        
        metrics = MockConvergenceMetrics(
            iteration=len(self.update_history),
            parameter_change=param_change,
            loss=loss,
            gradient_norm=gradient_norm,
            lipschitz_constant=self.lipschitz_constant,
            is_converged=is_converged
        )
        
        self.update_history.append(metrics)
        
        return metrics
    
    def _sample_parameter_space(self, sample_size: int) -> List[np.ndarray]:
        """Sample parameter space"""
        samples = []
        for _ in range(sample_size):
            sample = np.array([
                np.random.uniform(self.bounds[key]["min"], 
                                self.bounds[key]["max"])
                for key in sorted(self.bounds.keys())
            ])
            samples.append(sample)
        
        return samples


# Test Cases
class TestLipschitzContinuity:
    """Test Lipschitz Continuity Verification"""
    
    def test_contraction_mapping_verification(self):
        """Test contraction mapping verification"""
        bounds = {
            "weight": {"min": 0.0, "max": 1.0},
            "threshold": {"min": 0.5, "max": 0.95}
        }
        
        guarantee = MockParametricConvergenceGuarantee(bounds)
        
        # Contraction mapping: f(x) = 0.9 * x
        def update_function(params):
            return params * 0.9
        
        lipschitz_const = guarantee.verify_lipschitz_continuity(
            update_function
        )
        
        assert lipschitz_const < 1.0
        assert 0.85 < lipschitz_const < 0.95
    
    def test_non_contraction_mapping_detection(self):
        """Test non-contraction mapping detection"""
        bounds = {
            "param": {"min": 0.0, "max": 1.0}
        }
        
        guarantee = MockParametricConvergenceGuarantee(bounds)
        
        # Non-contraction mapping: f(x) = 1.5 * x
        def update_function(params):
            return params * 1.5
        
        with pytest.raises(ValueError, match="convergence not guaranteed"):
            guarantee.verify_lipschitz_continuity(update_function)
    
    def test_identity_mapping(self):
        """Test identity mapping"""
        bounds = {
            "param": {"min": 0.0, "max": 1.0}
        }
        
        guarantee = MockParametricConvergenceGuarantee(bounds)
        
        # Identity mapping: f(x) = x
        def update_function(params):
            return params
        
        lipschitz_const = guarantee.verify_lipschitz_continuity(
            update_function
        )
        
        # Lipschitz constant should be close to 1.0
        assert 0.95 < lipschitz_const <= 1.0


class TestConvergenceTimePrediction:
    """Test Convergence Time Prediction"""
    
    def test_convergence_time_calculation(self):
        """Test convergence time calculation"""
        bounds = {"param": {"min": 0.0, "max": 1.0}}
        guarantee = MockParametricConvergenceGuarantee(bounds)
        
        guarantee.lipschitz_constant = 0.5
        
        convergence_time = guarantee.predict_convergence_time(
            initial_error=1.0,
            target_error=1e-6
        )
        
        # Should be positive and reasonable
        assert convergence_time > 0
        assert convergence_time < 100
    
    def test_convergence_time_with_different_lipschitz_constants(self):
        """Test convergence time with different Lipschitz constants"""
        bounds = {"param": {"min": 0.0, "max": 1.0}}
        
        # Test with L = 0.5
        guarantee1 = MockParametricConvergenceGuarantee(bounds)
        guarantee1.lipschitz_constant = 0.5
        time1 = guarantee1.predict_convergence_time(1.0, 1e-6)
        
        # Test with L = 0.9
        guarantee2 = MockParametricConvergenceGuarantee(bounds)
        guarantee2.lipschitz_constant = 0.9
        time2 = guarantee2.predict_convergence_time(1.0, 1e-6)
        
        # Smaller Lipschitz constant should converge faster
        assert time1 < time2
    
    def test_convergence_time_without_lipschitz_constant(self):
        """Test convergence time prediction without Lipschitz constant"""
        bounds = {"param": {"min": 0.0, "max": 1.0}}
        guarantee = MockParametricConvergenceGuarantee(bounds)
        
        with pytest.raises(ValueError, match="Lipschitz constant not computed"):
            guarantee.predict_convergence_time(1.0, 1e-6)


class TestConvergenceMonitoring:
    """Test Convergence Monitoring"""
    
    def test_monitor_convergence_initial_state(self):
        """Test monitoring convergence in initial state"""
        bounds = {"param": {"min": 0.0, "max": 1.0}}
        guarantee = MockParametricConvergenceGuarantee(bounds)
        guarantee.lipschitz_constant = 0.5
        
        params = np.array([0.5])
        loss = 1.0
        gradient = np.array([0.1])
        
        metrics = guarantee.monitor_convergence(params, loss, gradient)
        
        assert metrics.iteration == 0
        assert metrics.parameter_change == np.inf
        assert metrics.is_converged is False
    
    def test_monitor_convergence_convergence_detection(self):
        """Test convergence detection"""
        bounds = {"param": {"min": 0.0, "max": 1.0}}
        guarantee = MockParametricConvergenceGuarantee(bounds)
        guarantee.lipschitz_constant = 0.5
        
        # First iteration
        params1 = np.array([0.5])
        guarantee.monitor_convergence(params1, 1.0, np.array([0.1]))
        
        # Second iteration - converged
        params2 = np.array([0.50001])
        metrics = guarantee.monitor_convergence(params2, 0.9, np.array([0.0001]))
        
        assert metrics.is_converged is True
    
    def test_monitor_convergence_history(self):
        """Test convergence history tracking"""
        bounds = {"param": {"min": 0.0, "max": 1.0}}
        guarantee = MockParametricConvergenceGuarantee(bounds)
        guarantee.lipschitz_constant = 0.5
        
        for i in range(5):
            params = np.array([0.5 + i * 0.01])
            loss = 1.0 - i * 0.1
            gradient = np.array([0.1 - i * 0.02])
            
            guarantee.monitor_convergence(params, loss, gradient)
        
        assert len(guarantee.update_history) == 5
        assert guarantee.update_history[0].iteration == 0
        assert guarantee.update_history[4].iteration == 4


class TestParameterSpaceSampling:
    """Test Parameter Space Sampling"""
    
    def test_sample_parameter_space_bounds(self):
        """Test parameter space sampling respects bounds"""
        bounds = {
            "weight": {"min": 0.0, "max": 1.0},
            "threshold": {"min": 0.5, "max": 0.95}
        }
        
        guarantee = MockParametricConvergenceGuarantee(bounds)
        samples = guarantee._sample_parameter_space(100)
        
        assert len(samples) == 100
        
        for sample in samples:
            assert 0.0 <= sample[0] <= 1.0
            assert 0.5 <= sample[1] <= 0.95
    
    def test_sample_parameter_space_randomness(self):
        """Test parameter space sampling produces different samples"""
        bounds = {
            "param": {"min": 0.0, "max": 1.0}
        }
        
        guarantee = MockParametricConvergenceGuarantee(bounds)
        samples1 = guarantee._sample_parameter_space(10)
        samples2 = guarantee._sample_parameter_space(10)
        
        # Samples should be different (with very high probability)
        assert not np.allclose(samples1, samples2)