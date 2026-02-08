from indestructibleautoops.graph import DAG, dag_is_acyclic, topological_sort


def test_dag_acyclic_ok():
    dag = DAG.from_nodes(
        [
            {"id": "a", "kind": "step", "run": "x", "deps": []},
            {"id": "b", "kind": "step", "run": "x", "deps": ["a"]},
        ]
    )
    assert dag_is_acyclic(dag) is True


def test_dag_cycle_fail():
    dag = DAG.from_nodes(
        [
            {"id": "a", "kind": "step", "run": "x", "deps": ["b"]},
            {"id": "b", "kind": "step", "run": "x", "deps": ["a"]},
        ]
    )
    assert dag_is_acyclic(dag) is False


def test_topological_sort_simple():
    """Test topological sort with a simple linear DAG."""
    dag = DAG.from_nodes(
        [
            {"id": "a", "kind": "step", "run": "x", "deps": []},
            {"id": "b", "kind": "step", "run": "x", "deps": ["a"]},
            {"id": "c", "kind": "step", "run": "x", "deps": ["b"]},
        ]
    )
    order = topological_sort(dag)
    assert order == ["a", "b", "c"]


def test_topological_sort_diamond():
    """Test topological sort with a diamond-shaped DAG."""
    dag = DAG.from_nodes(
        [
            {"id": "a", "kind": "step", "run": "x", "deps": []},
            {"id": "b", "kind": "step", "run": "x", "deps": ["a"]},
            {"id": "c", "kind": "step", "run": "x", "deps": ["a"]},
            {"id": "d", "kind": "step", "run": "x", "deps": ["b", "c"]},
        ]
    )
    order = topological_sort(dag)
    assert order is not None
    assert order[0] == "a"
    assert order[-1] == "d"
    assert set(order[1:3]) == {"b", "c"}


def test_topological_sort_cyclic():
    """Test that topological sort returns None for cyclic DAGs."""
    dag = DAG.from_nodes(
        [
            {"id": "a", "kind": "step", "run": "x", "deps": ["b"]},
            {"id": "b", "kind": "step", "run": "x", "deps": ["a"]},
        ]
    )
    order = topological_sort(dag)
    assert order is None


def test_topological_sort_multiple_roots():
    """Test topological sort with multiple nodes having no dependencies."""
    dag = DAG.from_nodes(
        [
            {"id": "a", "kind": "step", "run": "x", "deps": []},
            {"id": "b", "kind": "step", "run": "x", "deps": []},
            {"id": "c", "kind": "step", "run": "x", "deps": ["a", "b"]},
        ]
    )
    order = topological_sort(dag)
    assert order is not None
    assert set(order[:2]) == {"a", "b"}
    assert order[2] == "c"
