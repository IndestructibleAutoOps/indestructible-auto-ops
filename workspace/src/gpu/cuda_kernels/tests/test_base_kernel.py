"""
Tests for GL50 CUDA Kernels Module
"""

import sys
from pathlib import Path

import pytest

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from gpu.cuda_kernels.base_kernel import (
    ConvolutionKernel,
    KernelManager,
    MatrixMultiplicationKernel,
)


class TestMatrixMultiplicationKernel:
    """Test cases for MatrixMultiplicationKernel"""

    def test_kernel_initialization(self):
        """Test kernel initialization"""
        config = {'kernel_type': 'matrix_multiplication'}
        kernel = MatrixMultiplicationKernel(config)

        assert kernel.kernel_metadata['kernel_type'] == 'matrix_multiplication'
        assert not kernel.is_compiled

    def test_kernel_compile(self):
        """Test kernel compilation"""
        config = {'kernel_type': 'matrix_multiplication'}
        kernel = MatrixMultiplicationKernel(config)

        result = kernel.compile()
        assert result is True
        assert kernel.is_compiled
        assert 'compiled_at' in kernel.kernel_metadata

    def test_kernel_execute(self):
        """Test kernel execution"""
        config = {'kernel_type': 'matrix_multiplication'}
        kernel = MatrixMultiplicationKernel(config)
        kernel.compile()

        input_data = {
            'matrix_a': [[1, 2], [3, 4]],
            'matrix_b': [[5, 6], [7, 8]]
        }

        result = kernel.execute(input_data)
        assert result['status'] == 'SUCCESS'
        assert 'result' in result

    def test_kernel_execute_without_compile(self):
        """Test kernel execution without compilation"""
        config = {'kernel_type': 'matrix_multiplication'}
        kernel = MatrixMultiplicationKernel(config)

        input_data = {
            'matrix_a': [[1, 2]],
            'matrix_b': [[3, 4]]
        }

        with pytest.raises(RuntimeError):
            kernel.execute(input_data)

    def test_kernel_performance_metrics(self):
        """Test getting performance metrics"""
        config = {'kernel_type': 'matrix_multiplication'}
        kernel = MatrixMultiplicationKernel(config)
        kernel.compile()

        metrics = kernel.get_performance_metrics()
        assert 'execution_time_ms' in metrics
        assert 'memory_used_mb' in metrics


class TestConvolutionKernel:
    """Test cases for ConvolutionKernel"""

    def test_kernel_initialization(self):
        """Test kernel initialization"""
        config = {'kernel_type': 'convolution'}
        kernel = ConvolutionKernel(config)

        assert kernel.kernel_metadata['kernel_type'] == 'convolution'

    def test_kernel_compile(self):
        """Test kernel compilation"""
        config = {'kernel_type': 'convolution'}
        kernel = ConvolutionKernel(config)

        result = kernel.compile()
        assert result is True
        assert kernel.is_compiled

    def test_kernel_execute(self):
        """Test kernel execution"""
        config = {'kernel_type': 'convolution'}
        kernel = ConvolutionKernel(config)
        kernel.compile()

        input_data = {
            'input': [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
            'kernel': [[1, 0], [0, 1]]
        }

        result = kernel.execute(input_data)
        assert result['status'] == 'SUCCESS'


class TestKernelManager:
    """Test cases for KernelManager"""

    def test_manager_initialization(self):
        """Test manager initialization"""
        manager = KernelManager()

        assert len(manager.kernels) == 0

    def test_register_kernel(self):
        """Test kernel registration"""
        manager = KernelManager()
        config = {'kernel_type': 'matrix_multiplication'}
        kernel = MatrixMultiplicationKernel(config)

        kernel_id = manager.register_kernel(kernel)
        assert kernel_id in manager.kernels

    def test_compile_kernel(self):
        """Test compiling a kernel"""
        manager = KernelManager()
        config = {'kernel_type': 'matrix_multiplication'}
        kernel = MatrixMultiplicationKernel(config)

        kernel_id = manager.register_kernel(kernel)
        result = manager.compile_kernel(kernel_id)

        assert result is True
        assert kernel.is_compiled

    def test_execute_kernel(self):
        """Test executing a kernel"""
        manager = KernelManager()
        config = {'kernel_type': 'matrix_multiplication'}
        kernel = MatrixMultiplicationKernel(config)

        kernel_id = manager.register_kernel(kernel)
        manager.compile_kernel(kernel_id)

        input_data = {
            'matrix_a': [[1, 2]],
            'matrix_b': [[3, 4]]
        }

        result = manager.execute_kernel(kernel_id, input_data)
        assert result['status'] == 'SUCCESS'

    def test_list_kernels(self):
        """Test listing kernels"""
        manager = KernelManager()

        # Register multiple kernels
        for i in range(3):
            config = {'kernel_type': f'kernel_{i}'}
            kernel = MatrixMultiplicationKernel(config)
            manager.register_kernel(kernel)

        kernels = manager.list_kernels()
        assert len(kernels) == 3


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
