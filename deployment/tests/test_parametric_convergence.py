"""
测试参数化收敛性保证
"""
import pytest
import numpy as np
from typing import Callable, Dict, List
from dataclasses import dataclass
import math


@dataclass
class ConvergenceMetrics:
    """收敛指标"""
    iteration: int
    parameter_change: float
    loss: float
    gradient_norm: float
    lipschitz_constant: float
    is_converged: bool


class ParametricConvergenceGuarantee:
    """参数化收敛保证"""
    
    def __init__(self, parameter_space_bounds: Dict):
        self.bounds = parameter_space_bounds
        self.update_history: List[ConvergenceMetrics] = []
        self.lipschitz_constant = None
    
    def verify_lipschitz_continuity(
        self,
        update_function: Callable,
        sample_size: int = 100
    ) -> float:
        """验证 Lipschitz 连续性"""
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
    
    def predict_convergence_time(
        self,
        initial_error: float,
        target_error: float
    ) -> int:
        """预测收敛时间"""
        if self.lipschitz_constant is None:
            raise ValueError("Lipschitz constant not computed")
        
        n = math.log(target_error / initial_error) / math.log(
            self.lipschitz_constant
        )
        
        return int(np.ceil(n))
    
    def monitor_convergence(
        self,
        parameters: np.ndarray,
        loss: float,
        gradient: np.ndarray
    ) -> ConvergenceMetrics:
        """监控收敛"""
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
        
        metrics = ConvergenceMetrics(
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
        """在参数空间中采样"""
        samples = []
        for _ in range(sample_size):
            sample = np.array([
                np.random.uniform(self.bounds[key]["min"], 
                                self.bounds[key]["max"])
                for key in sorted(self.bounds.keys())
            ])
            samples.append(sample)
        
        return samples


# ============ 测试用例 ============

def test_lipschitz_continuity():
    """测试 Lipschitz 连续性"""
    bounds = {
        "weight": {"min": 0.0, "max": 1.0},
        "threshold": {"min": 0.5, "max": 0.95}
    }
    
    guarantee = ParametricConvergenceGuarantee(bounds)
    
    def update_function(params):
        return params * 0.9  # 收缩映射
    
    lipschitz_const = guarantee.verify_lipschitz_continuity(
        update_function
    )
    
    assert lipschitz_const < 1.0
    assert lipschitz_const > 0.85


def test_lipschitz_constant_too_large():
    """测试 Lipschitz 常数过大"""
    bounds = {"param": {"min": 0.0, "max": 1.0}}
    guarantee = ParametricConvergenceGuarantee(bounds)
    
    def update_function(params):
        return params * 1.5  # 扩张映射，不收敛
    
    with pytest.raises(ValueError):
        guarantee.verify_lipschitz_continuity(update_function)


def test_convergence_time_prediction():
    """测试收敛时间预测"""
    bounds = {"param": {"min": 0.0, "max": 1.0}}
    guarantee = ParametricConvergenceGuarantee(bounds)
    
    guarantee.lipschitz_constant = 0.5
    
    convergence_time = guarantee.predict_convergence_time(
        initial_error=1.0,
        target_error=1e-6
    )
    
    assert convergence_time > 0
    assert convergence_time < 100


def test_convergence_monitoring():
    """测试收敛监控"""
    bounds = {"param": {"min": 0.0, "max": 1.0}}
    guarantee = ParametricConvergenceGuarantee(bounds)
    guarantee.lipschitz_constant = 0.9
    
    # 模拟收敛过程
    params = np.array([0.5])
    for i in range(10):
        loss = 0.5 * (0.9 ** i)
        gradient = np.array([0.1 * (0.9 ** i)])
        
        metrics = guarantee.monitor_convergence(params, loss, gradient)
        
        if i > 5:
            assert metrics.parameter_change < 1e-3
    
    # 最后一轮应该收敛
    last_metrics = guarantee.update_history[-1]
    assert last_metrics.is_converged


def test_parameter_space_sampling():
    """测试参数空间采样"""
    bounds = {
        "param1": {"min": 0.0, "max": 1.0},
        "param2": {"min": 0.0, "max": 1.0}
    }
    guarantee = ParametricConvergenceGuarantee(bounds)
    
    samples = guarantee._sample_parameter_space(10)
    
    assert len(samples) == 10
    for sample in samples:
        assert sample.shape == (2,)
        assert np.all(sample >= 0.0)
        assert np.all(sample <= 1.0)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=.", "--cov-report=html"])
