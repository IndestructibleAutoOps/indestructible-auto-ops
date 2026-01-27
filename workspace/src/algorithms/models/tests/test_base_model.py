"""
Tests for GL40 Model Registry Module
"""

import sys
from pathlib import Path

import pytest

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from algorithms.models.base_model import BaseModel, ModelEvaluator, ModelRegistry


class MockModel(BaseModel):
    """Mock model for testing"""

    def train(self, training_data):
        return {'status': 'SUCCESS', 'accuracy': 0.95}

    def predict(self, input_data):
        return {'prediction': 'class_1', 'confidence': 0.9}

    def evaluate(self, test_data):
        return {'accuracy': 0.95, 'precision': 0.93, 'recall': 0.94}


class TestBaseModel:
    """Test cases for BaseModel"""

    def test_model_initialization(self):
        """Test model initialization"""
        config = {'model_type': 'mock_model'}
        model = MockModel(config)

        assert model.model_metadata['model_type'] == 'mock_model'
        assert model.model_metadata['status'] == 'INITIALIZED'
        assert not model.is_trained

    def test_model_train(self):
        """Test model training"""
        config = {'model_type': 'mock_model'}
        model = MockModel(config)

        result = model.train({'data': [1, 2, 3]})
        assert result['status'] == 'SUCCESS'

    def test_model_predict(self):
        """Test model prediction"""
        config = {'model_type': 'mock_model'}
        model = MockModel(config)

        result = model.predict({'input': [1, 2, 3]})
        assert 'prediction' in result

    def test_model_evaluate(self):
        """Test model evaluation"""
        config = {'model_type': 'mock_model'}
        model = MockModel(config)

        result = model.evaluate({'test_data': [1, 2, 3]})
        assert 'accuracy' in result

    def test_model_save(self):
        """Test model saving"""
        config = {'model_type': 'mock_model'}
        model = MockModel(config)

        result = model.save_model('/tmp/test_model.pkl')
        assert result is True
        assert 'saved_at' in model.model_metadata


class TestModelRegistry:
    """Test cases for ModelRegistry"""

    def test_registry_initialization(self):
        """Test registry initialization"""
        registry = ModelRegistry()

        assert len(registry.models) == 0
        assert len(registry.model_versions) == 0

    def test_register_model(self):
        """Test model registration"""
        registry = ModelRegistry()
        config = {'model_type': 'mock_model'}
        model = MockModel(config)

        model_id = registry.register_model(model)
        assert model_id in registry.models
        assert registry.model_versions[model_id] == 1

    def test_get_model(self):
        """Test getting a model"""
        registry = ModelRegistry()
        config = {'model_type': 'mock_model'}
        model = MockModel(config)

        model_id = registry.register_model(model)
        retrieved_model = registry.get_model(model_id)

        assert retrieved_model is not None
        assert retrieved_model.model_metadata['model_type'] == 'mock_model'

    def test_list_models(self):
        """Test listing models"""
        registry = ModelRegistry()

        # Register multiple models
        for i in range(3):
            config = {'model_type': f'mock_model_{i}'}
            model = MockModel(config)
            registry.register_model(model)

        models = registry.list_models()
        assert len(models) == 3

    def test_update_model(self):
        """Test updating a model"""
        registry = ModelRegistry()
        config = {'model_type': 'mock_model'}
        model = MockModel(config)

        model_id = registry.register_model(model)
        original_version = registry.model_versions[model_id]

        # Update model
        config['model_type'] = 'updated_model'
        updated_model = MockModel(config)
        success = registry.update_model(model_id, updated_model)

        assert success is True
        assert registry.model_versions[model_id] == original_version + 1


class TestModelEvaluator:
    """Test cases for ModelEvaluator"""

    def test_evaluator_initialization(self):
        """Test evaluator initialization"""
        evaluator = ModelEvaluator()

        assert len(evaluator.evaluation_history) == 0

    def test_evaluate_model(self):
        """Test model evaluation"""
        evaluator = ModelEvaluator()
        config = {'model_type': 'mock_model'}
        model = MockModel(config)

        result = evaluator.evaluate(model, {'test_data': [1, 2, 3]})
        assert 'metrics' in result
        assert result['metrics']['accuracy'] == 0.95
        assert len(evaluator.evaluation_history) == 1

    def test_get_evaluation_history(self):
        """Test getting evaluation history"""
        evaluator = ModelEvaluator()
        config = {'model_type': 'mock_model'}
        model = MockModel(config)

        # Evaluate multiple times
        for i in range(3):
            evaluator.evaluate(model, {'test_data': [i]})

        history = evaluator.get_evaluation_history(model.model_metadata['model_id'])
        assert len(history) == 3


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
