"""Tests to verify that the engine execution order is derived from the DAG."""

from pathlib import Path

import yaml

from indestructibleautoops.engine import Engine
from indestructibleautoops.graph import DAG, topological_sort


def test_topological_sort_matches_default_dag():
    """Test that topological sort produces correct order for default DAG."""
    # Load the default pipeline config
    default_cfg_path = Path("configs/indestructibleautoops.pipeline.yaml").resolve()
    with open(default_cfg_path, encoding="utf-8") as f:
        config = yaml.safe_load(f)
    
    # Get DAG nodes
    dag_nodes = config["spec"]["dag"]["nodes"]
    dag = DAG.from_nodes(dag_nodes)
    
    # Get topological order
    order = topological_sort(dag)
    
    # Verify the expected linear order (since it's a chain)
    expected_order = [
        "interface_metadata_parse",
        "parameter_validation",
        "permission_resolution",
        "security_assessment",
        "approval_chain_validation",
        "tool_execution",
        "history_immutable",
        "continuous_monitoring",
    ]
    assert order == expected_order


def test_engine_execution_order_matches_dag(tmp_path: Path):
    """
    Test that the engine execution order matches the DAG topological order.
    
    This verifies that the engine derives execution order from the configured
    DAG rather than using a hard-coded sequence.
    """
    # Create a minimal project structure
    (tmp_path / "README.md").write_text("x", encoding="utf-8")
    
    # Use the default config
    cfg_path = Path("configs/indestructibleautoops.pipeline.yaml").resolve()
    
    # Create engine
    engine = Engine.from_config(cfg_path, tmp_path, mode="plan")
    
    # Track the execution order by patching the event emission
    execution_order = []
    original_emit = engine.events.emit
    
    def track_emit(trace_id, step_id, event_type, data=None):
        if event_type == "start":
            execution_order.append(step_id)
        return original_emit(trace_id, step_id, event_type, data)
    
    engine.events.emit = track_emit
    
    # Run the engine
    result = engine.run()
    assert result["ok"] is True
    
    # Verify execution order matches DAG topological order
    with open(cfg_path, encoding="utf-8") as f:
        config = yaml.safe_load(f)
    
    dag_nodes = config["spec"]["dag"]["nodes"]
    dag = DAG.from_nodes(dag_nodes)
    expected_order = topological_sort(dag)
    
    assert execution_order == expected_order


def test_alternative_dag_order():
    """Test topological sort with a modified DAG structure."""
    # Create a DAG with parallel steps
    dag_nodes = [
        {"id": "step_a", "kind": "step", "run": "x", "deps": []},
        {"id": "step_b", "kind": "step", "run": "x", "deps": []},
        {"id": "step_c", "kind": "step", "run": "x", "deps": ["step_a", "step_b"]},
    ]
    dag = DAG.from_nodes(dag_nodes)
    order = topological_sort(dag)
    
    # step_c must come after both step_a and step_b
    assert order.index("step_c") > order.index("step_a")
    assert order.index("step_c") > order.index("step_b")
    # step_a and step_b can be in either order (both are roots)
    assert set(order[:2]) == {"step_a", "step_b"}
    assert order[2] == "step_c"

