# FILE: tests/integration/test_ng_governance_integration.py
# 集成測試：NG 治理系統

import pytest
import numpy as np
from typing import Dict, List


class TestNgGovernanceIntegration:
    """Integration Tests for NG Governance System"""
    
    def test_end_to_end_semantic_binding_workflow(self):
        """Test end-to-end semantic binding workflow"""
        # 1. Create semantic binding manager
        from tests.unit.test_ng_semantic_binding import MockNgVectorSpaceManager, MockNgSemanticBinding
        
        manager = MockNgVectorSpaceManager()
        
        # 2. Register multiple entities
        entities = [
            MockNgSemanticBinding("evidence_001", "NG70600", "semantic_entity", "evidence"),
            MockNgSemanticBinding("hypothesis_001", "NG60100", "business_intent", "hypothesis"),
            MockNgSemanticBinding("cluster_001", "NG70700", "semantic_entity", "cluster"),
        ]
        
        for entity in entities:
            assert manager.register_entity(entity) is True
        
        # 3. Verify consistency
        assert manager.verify_embedding_space_consistency() is True
        
        # 4. Retrieve entities
        for entity in entities:
            retrieved = manager.get_binding(entity.entity_id)
            assert retrieved is not None
            assert retrieved.ng_code == entity.ng_code
    
    def test_parametric_convergence_with_multiple_iterations(self):
        """Test parametric convergence with multiple iterations"""
        from tests.unit.test_parametric_convergence import MockParametricConvergenceGuarantee
        
        bounds = {
            "weight": {"min": 0.0, "max": 1.0},
            "threshold": {"min": 0.5, "max": 0.95}
        }
        
        guarantee = MockParametricConvergenceGuarantee(bounds)
        
        # Verify Lipschitz continuity
        def update_function(params):
            return params * 0.8
        
        lipschitz_const = guarantee.verify_lipschitz_continuity(
            update_function
        )
        
        assert lipschitz_const < 1.0
        
        # Predict convergence time
        convergence_time = guarantee.predict_convergence_time(1.0, 1e-6)
        assert convergence_time > 0
        
        # Monitor convergence
        for i in range(convergence_time + 10):
            params = np.array([0.5, 0.7])
            loss = 1.0 * (lipschitz_const ** i)
            gradient = np.array([0.1, 0.05])
            
            metrics = guarantee.monitor_convergence(params, loss, gradient)
            
            if i >= convergence_time:
                # Should converge after predicted time
                assert metrics.is_converged is True
    
    def test_fallback_validation_with_recovery_protocol(self):
        """Test fallback validation with recovery protocol"""
        from tests.unit.test_fallback_semantic_validation import (
            MockFallbackSemanticValidator, MockEmbeddingModel
        )
        
        model = MockEmbeddingModel()
        validator = MockFallbackSemanticValidator(model)
        
        # Original intent
        original_intent = "maximize-quantum-fidelity NG60100"
        
        # Fallback decisions at different levels
        fallback_decisions = {
            "level_1": {"action": "advanced", "NG60100": True, "NG70600": True},
            "level_2": {"action": "basic", "NG60100": True},
            "level_3": {"action": "heuristic", "NG60100": True},
        }
        
        safety_constraints = [
            lambda d: "action" in d,
            lambda d: "NG60100" in d
        ]
        
        # Validate each level
        for level, decision in fallback_decisions.items():
            is_valid, results = validator.validate_fallback_decision(
                original_intent,
                decision,
                safety_constraints
            )
            
            assert results["safety_preserved"] is True
            assert results["semantic_anchor_preserved"] is True
    
    def test_cross_component_consistency(self):
        """Test cross-component consistency"""
        from tests.unit.test_ng_semantic_binding import MockNgVectorSpaceManager, MockNgSemanticBinding
        from tests.unit.test_parametric_convergence import MockParametricConvergenceGuarantee
        from tests.unit.test_fallback_semantic_validation import MockFallbackSemanticValidator, MockEmbeddingModel
        
        # 1. Semantic binding
        binding_manager = MockNgVectorSpaceManager()
        binding = MockNgSemanticBinding(
            "entity_001", "NG70600", "semantic_entity", "evidence"
        )
        binding_manager.register_entity(binding)
        
        # 2. Parametric convergence
        bounds = {"param": {"min": 0.0, "max": 1.0}}
        convergence_guarantee = MockParametricConvergenceGuarantee(bounds)
        
        def update_func(p):
            return p * 0.9
        
        lipschitz = convergence_guarantee.verify_lipschitz_continuity(update_func)
        
        # 3. Fallback validation
        model = MockEmbeddingModel()
        validator = MockFallbackSemanticValidator(model)
        
        # All components should work together
        assert binding_manager.verify_embedding_space_consistency() is True
        assert lipschitz < 1.0
        
        # Validate fallback with semantic binding
        fallback_decision = {
            "action": "fallback",
            "NG70600": True,
            "ng_code": binding.ng_code
        }
        
        safety_constraints = [lambda d: "action" in d]
        
        is_valid, results = validator.validate_fallback_decision(
            "test NG70600",
            fallback_decision,
            safety_constraints
        )
        
        assert results["safety_preserved"] is True